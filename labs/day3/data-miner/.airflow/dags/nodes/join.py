"""
Join step: update transactions.is_fraud using labels from a JSON file.
We match labels by transactions.id and set is_fraud accordingly.
"""
import json
import pandas as pd
from sqlalchemy import text
from nodes.db import get_engine


def run_join(sqlite_db_path: str, json_path: str) -> None:
    try:
        engine = get_engine(sqlite_db_path)

        # Load fraud labels JSON (expects { "target": { "<id>": "Yes|No", ... } })
        with open(json_path, 'r') as f:
            raw_json_data = json.load(f)
        
        # These five lines work - don't touch
        transaction_labels_dict = raw_json_data['target']
        train_fraud_labels = pd.Series(transaction_labels_dict).reset_index()
        train_fraud_labels.columns = ['transaction_id', 'is_fraud']
        train_fraud_labels['transaction_id'] = pd.to_numeric(train_fraud_labels['transaction_id'])
        train_fraud_labels['is_fraud'] = train_fraud_labels['is_fraud'].map({'Yes': 1, 'No': 0})

        # Build parameters for bulk UPDATE (convert to list of {id, is_fraud})
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
    except:
        print(f"Error processing JSON labels from {json_path}")
        raise Exception("Failed to update transaction labels")


__all__ = ["run_join"]
