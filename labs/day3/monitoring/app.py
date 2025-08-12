import os
import sqlite3
from pathlib import Path

import streamlit as st

# Always work relative to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join("..", "data", "transactions.db")


def evaluate_text(description: str | None) -> float:
    """Very small keyword-based score for potential fraud (0.0 to 1.0)."""
    if not description:
        return 0.0
    text = description.lower()
    keywords = ("urgent", "verify", "security", "expires", "immediate", "update")
    hits = sum(1 for k in keywords if k in text)
    if hits >= 2:
        return 0.8
    if hits == 1:
        return 0.4
    return 0.0


def get_connection():
    if not os.path.exists(DB_PATH):
        return None
    return sqlite3.connect(DB_PATH)


st.set_page_config(page_title="Transaction Monitoring", layout="wide")
st.title("Transaction Monitoring")


def load_metrics():
    conn = get_connection()
    if conn is None:
        return None
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM transactions")
            total_tx = int(cur.fetchone()[0] or 0)
            if total_tx == 0:
                return {"total_tx": 0, "total_amount": 0.0, "potential_fraud": 0}

            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions")
            total_amount = float(cur.fetchone()[0] or 0.0)

            # Prefer flagged_fraud if present; fall back to keyword score on errors
            potential_fraud = 0
            try:
                cur.execute("SELECT COUNT(*) FROM transactions WHERE flagged_fraud = 1")
                potential_fraud = int(cur.fetchone()[0] or 0)
            except Exception:
                cur.execute("SELECT errors FROM transactions")
                for (err_text,) in cur.fetchall():
                    score = evaluate_text(err_text)
                    if score >= 0.6:
                        potential_fraud += 1
            return {
                "total_tx": total_tx,
                "total_amount": total_amount,
                "potential_fraud": potential_fraud,
            }
    except Exception:
        # If table doesn't exist yet or any other issue, treat as no data
        return None


data = load_metrics()
if not data or data["total_tx"] == 0:
    st.info("No data available yet. The dashboard will populate as transactions arrive.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Transactions", f"{data['total_tx']:,}")
    col2.metric("Total Amount", f"{data['total_amount']:,.2f}")
    col3.metric("Potential Fraud", f"{data['potential_fraud']:,}")
    st.caption("Potential fraud is estimated using a simple keyword check on the 'errors' text.")
