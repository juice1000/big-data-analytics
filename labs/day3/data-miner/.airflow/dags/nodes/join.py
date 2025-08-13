"""Task node: JOIN

Purpose:
    Update ground‑truth labels (is_fraud) for existing transactions using an
    offline JSON labels file keyed by transaction id.

Critical invariant: DO NOT touch the 5 canonical lines that parse & map labels;
they are verified against earlier notebook experimentation for consistency.
"""
import json
import pandas as pd
from sqlalchemy import text
from nodes.db import get_engine


def run_join(sqlite_db_path: str, json_path: str) -> None:
    try:
        engine = get_engine(sqlite_db_path)

    # Load labels JSON (shape: {"target": {"<id>": "Yes"|"No", ...}}).
        with open(json_path, 'r') as f:
            raw_json_data = json.load(f)
        
    # Canonical transformation block (DO NOT MODIFY): maps Yes/No -> 1/0 int flags.
        transaction_labels_dict = raw_json_data['target']
        train_fraud_labels = pd.Series(transaction_labels_dict).reset_index()
        train_fraud_labels.columns = ['transaction_id', 'is_fraud']
        train_fraud_labels['transaction_id'] = pd.to_numeric(train_fraud_labels['transaction_id'])
        train_fraud_labels['is_fraud'] = train_fraud_labels['is_fraud'].map({'Yes': 1, 'No': 0})

    # Build parameters for bulk UPDATE (parameterized to avoid SQL injection / improve batching).
        params = (
            train_fraud_labels
            .rename(columns={"transaction_id": "id"})
            [["id", "is_fraud"]]
            .astype(int)
            .to_dict(orient="records")
        )

        if params:
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE transactions SET is_fraud = :is_fraud WHERE id = :id"),
                    params,
                )
    except Exception as e:
        print(f"Error processing JSON labels from {json_path}: {e}")
        raise Exception("Failed to update transaction labels")


__all__ = ["run_join"]
