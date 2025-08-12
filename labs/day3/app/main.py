from contextlib import asynccontextmanager

from evaluator import evaluate_text
from fastapi import FastAPI
from models import Decision, Transaction
from storage import init_db, insert_transaction
from whitelist import amount_is_unusual


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    yield


app = FastAPI(title="Fraud Detection API", lifespan=lifespan)


@app.post("/transaction", response_model=Decision)
def process_transaction(tx: Transaction):
    # Simple rules: amount deviation + text keywords
    amt_unusual, amt_score = amount_is_unusual(tx.client_id, tx.amount)
    # If there's no description field in the schema, fall back to errors text
    desc = getattr(tx, "description", None)
    if not desc:
        desc = tx.errors
    txt_score, txt_reason = evaluate_text(desc)

    score = min(1.0, 0.6 * txt_score + 0.4 * amt_score)
    suspicious = score >= 0.6 or amt_unusual

    reason = ", ".join(filter(None, ["amount unusual" if amt_unusual else None, txt_reason])) or "ok"

    decision = Decision(suspicious=suspicious, reason=reason, score=round(score, 3))

    # Persist including flagged_fraud and is_fraud if provided
    # If caller didn't provide flagged_fraud, set from decision
    if tx.flagged_fraud is None:
        tx.flagged_fraud = decision.suspicious
    # Persist the Pydantic model directly
    insert_transaction(tx)

    return decision


if __name__ == "__main__":
    import uvicorn

    # Run the already-constructed app instance to avoid import path issues
    uvicorn.run(app, host="0.0.0.0", port=8080)
