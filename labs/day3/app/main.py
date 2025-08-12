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
    # Persist as-is
    tx_id = insert_transaction(tx.model_dump())

    # Simple rules: amount deviation + text keywords
    amt_unusual, amt_score = amount_is_unusual(tx.client_id, tx.amount)
    txt_score, txt_reason = evaluate_text(tx.description)

    score = min(1.0, 0.6 * txt_score + 0.4 * amt_score)
    suspicious = score >= 0.6 or amt_unusual

    reason = ", ".join(filter(None, ["amount unusual" if amt_unusual else None, txt_reason])) or "ok"

    return Decision(suspicious=suspicious, reason=reason, score=round(score, 3))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
