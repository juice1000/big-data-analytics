import sqlite3
from pathlib import Path
from typing import Any, Mapping, Union

from models import Transaction
from sqlmodel import Session, SQLModel, create_engine

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "transactions.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
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
