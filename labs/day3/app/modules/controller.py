from db.models import Decision, Transaction
from db.storage import insert_transaction
from modules.evaluator import evaluate_text
from modules.whitelist import amount_is_unusual


def process_transaction_logic(tx: Transaction) -> Decision:
    """Business logic for processing a transaction and returning a fraud decision."""
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

    # If caller didn't provide flagged_fraud, set from decision
    if tx.flagged_fraud is None:
        tx.flagged_fraud = decision.suspicious

    # Persist the transaction
    insert_transaction(tx)

    return decision
