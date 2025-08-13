from db.models import Decision, Transaction
from db.storage import insert_transaction
from modules.whitelist.whitelister import amount_is_unusual, evaluate_transaction


def process_transaction_logic(tx: Transaction) -> Decision:
    """Primary business logic for evaluating a transaction.

    Steps:
    1) Evaluate fraud heuristics/LLM and produce a decision with a short reason.
    2) Mirror the decision into tx.flagged_fraud for downstream monitoring.
    3) Persist the transaction to SQLite for analytics (Streamlit dashboard, etc.).

    We do not set tx.is_fraud here; that ground-truth label is derived offline by the
    data pipeline (join step) and written later, enabling model monitoring.
    """

    suspicious, reason = evaluate_transaction(tx)
    decision = Decision(suspicious=suspicious, reason=reason)
    # If caller didn't provide flagged_fraud, set from decision
    tx.flagged_fraud = suspicious

    # Persist the transaction for observability and later labeling/joins
    insert_transaction(tx)
    return decision
