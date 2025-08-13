from typing import Tuple

from modules.whitelist.llm_whitelist import analyze_transaction_with_llm
from modules.whitelist.heuristic_whitelist import amount_is_unusual


def evaluate_transaction(tx: dict | None) -> Tuple[float, str]:
    """Combine fast heuristics with an LLM check to produce a decision.

    Policy:
    - If amount looks unusual OR we don't have enough history (None), we escalate to LLM.
    - If the LLM flags fraud, we return True with its reason; otherwise we return False.
    - Keep thresholds conservative in the lab to demonstrate both paths.
    """
    if tx is None:
        return 0.0, "Invalid transaction"

    flagged_fraud = amount_is_unusual(getattr(tx, "client_id"), getattr(tx, "amount", 0.0))

    if flagged_fraud or flagged_fraud is None:  # escalate if unusual or insufficient data
        is_fraud, reason = analyze_transaction_with_llm(getattr(tx, "description"))
        print("llm is_fraud:", is_fraud, "reason:", reason)
        if is_fraud:  # LLM suspects fraud
            return True, reason
    return False, "Transaction is normal"
