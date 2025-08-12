from contextlib import asynccontextmanager

from controller import process_transaction_logic
from fastapi import FastAPI
from models import Decision, Transaction
from storage import init_db, reset_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    yield


app = FastAPI(title="Fraud Detection API", lifespan=lifespan)


@app.post("/transaction", response_model=Decision)
def process_transaction(tx: Transaction):
    """Process a transaction and return fraud decision."""
    return process_transaction_logic(tx)


@app.get("/reset-db")
def reset_db():
    """Delete and recreate the database."""
    reset_database()
    return {"message": "Database reset successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
