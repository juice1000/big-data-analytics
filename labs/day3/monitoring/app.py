import os
import sqlite3
import pandas as pd

import streamlit as st

# Always work relative to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join("..", "data", "transactions.db")

# TODO: rewrite for SQLModel

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
                return {"total_tx": 0, "total_amount": 0.0, "potential_fraud": 0, "is_fraud_count": 0}

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

            # Count of labeled frauds (is_fraud == 1), if column exists
            is_fraud_count = 0
            try:
                cur.execute("SELECT COUNT(*) FROM transactions WHERE is_fraud = 1")
                is_fraud_count = int(cur.fetchone()[0] or 0)
            except Exception:
                is_fraud_count = None
            return {
                "total_tx": total_tx,
                "total_amount": total_amount,
                "potential_fraud": potential_fraud,
                "is_fraud_count": is_fraud_count,
            }
    except Exception:
        # If table doesn't exist yet or any other issue, treat as no data
        return None


data = load_metrics()
if not data or data["total_tx"] == 0:
    st.info("No data available yet. The dashboard will populate as transactions arrive.")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Transactions", f"{data['total_tx']:,}")
    col2.metric("Total Amount", f"{data['total_amount']:,.2f}")
    col3.metric("Potential Fraud", f"{data['potential_fraud']:,}")
    col4.metric("Is Fraud", "N/A" if data.get("is_fraud_count") is None else f"{data['is_fraud_count']:,}")
    st.caption("Potential fraud uses flagged_fraud when available, else a simple keyword check. 'Is Fraud' reflects labeled ground truth if loaded.")

    # Recent transactions table (20 rows)
    def load_recent_transactions(limit: int = 20, only_flagged: bool = False, only_is_fraud: bool = False):
        conn = get_connection()
        if conn is None:
            return None
        try:
            with conn:
                base = (
                    "SELECT id, date, client_id, card_id, amount, currency, "
                    "merchant_city, mcc, description, flagged_fraud, is_fraud "
                    "FROM transactions"
                )
                where_clauses = []
                if only_flagged:
                    where_clauses.append("flagged_fraud = 1")
                if only_is_fraud:
                    where_clauses.append("is_fraud = 1")
                if where_clauses:
                    base += " WHERE " + " AND ".join(where_clauses)
                query = base + " ORDER BY id DESC LIMIT ?"
                return pd.read_sql_query(query, conn, params=(limit,))
        except Exception:
            # Fallback: try without WHERE and filter in pandas if possible
            try:
                with conn:
                    df = pd.read_sql_query(
                        base + " ORDER BY id DESC LIMIT ?", conn, params=(limit,)
                    )
                if only_flagged and "flagged_fraud" in df.columns:
                    ser_f = df["flagged_fraud"].fillna(0)
                    try:
                        ser_f = ser_f.astype(int)
                    except Exception:
                        ser_f = ser_f.apply(lambda x: 1 if str(x).lower() in ("true", "1") else 0)
                    df = df[ser_f == 1]
                if only_is_fraud and "is_fraud" in df.columns:
                    ser_i = df["is_fraud"].fillna(0)
                    try:
                        ser_i = ser_i.astype(int)
                    except Exception:
                        ser_i = ser_i.apply(lambda x: 1 if str(x).lower() in ("true", "1") else 0)
                    df = df[ser_i == 1]
                return df
            except Exception:
                return None

    only_flagged = st.checkbox("Show only flagged_fraud = 1", value=False)
    only_is_fraud = st.checkbox("Show only is_fraud = 1", value=False)
    recent_df = load_recent_transactions(20, only_flagged=only_flagged, only_is_fraud=only_is_fraud)
    st.subheader("Recent transactions (latest 20)")
    if recent_df is None or recent_df.empty:
        st.write("No recent transactions to display.")
    else:
        st.dataframe(recent_df, use_container_width=True, height=400)
