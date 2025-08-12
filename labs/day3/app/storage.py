import os
import sqlite3
from os.path import abspath, dirname, exists, join
from typing import Any, Mapping, Union

from models import Transaction
from sqlmodel import Session, SQLModel, create_engine

DB_PATH = abspath(join(dirname(__file__), "..", "data", "transactions.db"))
print(f"Database path: {DB_PATH}")
if not exists(dirname(DB_PATH)):
    os.makedirs(dirname(DB_PATH), exist_ok=True)
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    if not exists(dirname(DB_PATH)):
        os.makedirs(dirname(DB_PATH), exist_ok=True)
    SQLModel.metadata.create_all(ENGINE)


def get_session() -> Session:
    return Session(ENGINE)


def insert_transaction(tx: Union[Transaction, Mapping[str, Any]]) -> int:
    if not isinstance(tx, Transaction):
        tx = Transaction(**tx)  # type: ignore[arg-type]
    with get_session() as session:
        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx.id or 0


def reset_database():
    """Delete and recreate the database schema."""
    if exists(DB_PATH):
        print(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)
        init_db()
