"""
FastAPI entrypoint for the Fraud Detection API.

Key ideas documented here:
- We load environment variables early so dependencies (e.g., LLM helper) can pick up API keys.
- We initialize the database in the FastAPI lifespan so tables exist before the first request.
- We keep the HTTP layer thin: endpoint -> controller with business logic -> persistence.

This separation keeps the app testable and makes swapping implementations easy
(e.g., different storage backends or different fraud strategies).
"""

from contextlib import asynccontextmanager

from db.models import Decision, Transaction
from db.storage import init_db, reset_database
from dotenv import load_dotenv
from fastapi import FastAPI
from modules.controller import process_transaction_logic

# Load environment variables from .env file so downstream modules (like the LLM helper)
# can access secrets such as OPENAI_API_KEY via os.getenv without manual export.
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan hook.

    We create the SQLite schema on startup to ensure the API can accept writes even
    on a clean workspace. This avoids ordering issues where the first request fails
    because the DB tables haven't been created yet.
    """
    # Initialize database on startup (idempotent with SQLModel.create_all)
    init_db()
    yield


# Expose a simple, well-named API for the lab. The title helps in the auto-generated docs.
app = FastAPI(title="Fraud Detection API", lifespan=lifespan)


@app.post("/transaction", response_model=Decision)
def process_transaction(tx: Transaction):
    """Process a transaction and return a fraud decision.

    Contract:
    - Input: Transaction payload (validated by Pydantic/SQLModel)
    - Output: Decision(suspicious: bool, reason: str)
    - Side-effect: persists the transaction to SQLite for monitoring/analytics.
    """
    return process_transaction_logic(tx)


@app.get("/reset-db")
def reset_db():
    """Dangerous but handy: delete and recreate the local SQLite database.

    Useful for local development to clear state quickly. Avoid exposing this in
    production without authentication.
    """
    reset_database()
    return {"message": "Database reset successfully"}


if __name__ == "__main__":
    # Local dev convenience: run with reload so code edits reflect without restart.
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
