from typing import Tuple

from db.storage import get_session
from modules.whitelist.llm_whitelist import analyze_transaction_with_llm
from sqlmodel import text


def analyze_transaction(tx: dict) -> Tuple[bool, str]:
    description = getattr(tx, "description", None)
    llm_result = analyze_transaction_with_llm(description)
    is_fraud = llm_result.get("is_fraud", False)
    reason = llm_result.get("reason", "Unknown")
    return is_fraud, reason


# Very simple amount-based deviation check using client's history
def amount_is_unusual(client_id: str, amount: float, factor: float = 3.0) -> bool:
    with get_session() as session:
        result = session.exec(
            text("SELECT AVG(amount) as avg_amt, COUNT(*) as cnt FROM transactions WHERE client_id = :cid").params(
                cid=client_id
            )
        )

        row = result.first()
        if not row:
            return False
        avg_amt, cnt = row[0], row[1]
        if avg_amt is None or (cnt or 0) < 3:
            return False
        avg = float(avg_amt)
        diff_ratio = abs(amount - avg) / (avg if avg else 1.0)
        return diff_ratio > factor

def evaluate_transaction(tx: dict | None) -> Tuple[float, str]:
    if tx is None:
        return 0.0, "Invalid transaction"
    flagged_fraud = amount_is_unusual(getattr(tx,"client_id"), getattr(tx,"amount", 0.0))
    if flagged_fraud:  # Check if the amount is unusual
        return True, "Unusual transaction amount"
    flagged_fraud, reason = analyze_transaction(tx)
    if flagged_fraud:  # Check if the transaction is fraudulent
        return True, reason
    return False, "Transaction is normal"
