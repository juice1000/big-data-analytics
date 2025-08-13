from typing import Tuple

from modules.whitelist.llm_whitelist import analyze_transaction_with_llm
from modules.whitelist.heuristic_whitelist import amount_is_unusual

def evaluate_transaction(tx: dict | None) -> Tuple[float, str]:
    if tx is None:
        return 0.0, "Invalid transaction"
    flagged_fraud = amount_is_unusual(getattr(tx,"client_id"), getattr(tx,"amount", 0.0))
    if flagged_fraud or flagged_fraud is None:  # Check if the amount is unusual
        is_fraud, reason = analyze_transaction_with_llm(getattr(tx,"description"))
        print("llm is_fraud:", is_fraud, "reason:", reason)
        if is_fraud:  # Check if the transaction is fraudulent
            return True, reason
    return False, "Transaction is normal"
