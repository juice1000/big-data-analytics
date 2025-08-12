from db.models import Decision, Transaction
from db.storage import insert_transaction
from modules.whitelist.whitelister import amount_is_unusual, evaluate_transaction


def process_transaction_logic(tx: Transaction) -> Decision:
    """Business logic for processing a transaction and returning a fraud decision."""

    suspicious, reason = evaluate_transaction(tx)
    decision = Decision(suspicious=suspicious, reason=reason)

    # If caller didn't provide flagged_fraud, set from decision
    tx.flagged_fraud = suspicious

    # Persist the transaction
    insert_transaction(tx)

    return decision
