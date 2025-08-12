from typing import Tuple

from db.storage import get_session
from modules.whitelist.llm_whitelist import analyze_transaction_with_llm
from modules.whitelist.heuristic_whitelist import amount_is_unusual
from sqlmodel import text




def evaluate_transaction(tx: dict | None) -> Tuple[float, str]:
    if tx is None:
        return 0.0, "Invalid transaction"
    flagged_fraud = amount_is_unusual(getattr(tx,"client_id"), getattr(tx,"amount", 0.0))
    if flagged_fraud:  # Check if the amount is unusual
        return True, "Unusual transaction amount"
    is_fraud, reason = analyze_transaction_with_llm(description)
    if flagged_fraud:  # Check if the transaction is fraudulent
        return True, reason
    return False, "Transaction is normal"
