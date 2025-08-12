import sqlite3
from pathlib import Path
from typing import Optional, Tuple

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "transactions.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    client_id TEXT,
    card_id TEXT,
    amount REAL,
    use_chip TEXT,
    merchant_id TEXT,
    merchant_city TEXT,
    merchant_state TEXT,
    zip TEXT,
    mcc INTEGER,
    errors TEXT
);
CREATE INDEX IF NOT EXISTS idx_client_id ON transactions(client_id);
"""


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()


def insert_transaction(tx: dict) -> int:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO transactions (
                date, client_id, card_id, amount, use_chip, merchant_id,
                merchant_city, merchant_state, zip, mcc, errors
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tx.get("date"),
                tx.get("client_id"),
                tx.get("card_id"),
                tx.get("amount"),
                tx.get("use_chip"),
                tx.get("merchant_id"),
                tx.get("merchant_city"),
                tx.get("merchant_state"),
                tx.get("zip"),
                tx.get("mcc"),
                tx.get("errors"),
            ),
        )
        conn.commit()
        return cur.lastrowid
