"""Storage utilities built on SQLModel/SQLite.

Design choices:
- Use SQLModel engine globally for simplicity in a small app; it's thread-safe for typical
    FastAPI usage. For larger scale, consider per-request sessions via dependencies.
- Keep an explicit reset_database() handy for the lab to nuke local state quickly.
- Provide both SQLModel sessions and a raw sqlite3 connection for ad-hoc operations
    (e.g., when you need sqlite3-specific pragmas or bulk ops). Prefer sessions for ORM flows.
"""

import os
import sqlite3
from os.path import abspath, dirname, exists, join
from typing import Any, Mapping, Union

from db.models import Transaction
from sqlmodel import Session, SQLModel, create_engine

DB_PATH = abspath(join(dirname(__file__), "..", "..", "data", "transactions.db"))
if not exists(dirname(DB_PATH)):
    os.makedirs(dirname(DB_PATH), exist_ok=True)
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def get_conn():
    """Return a raw sqlite3 connection.

    Useful for low-level operations or when integrating with libraries that expect a
    DB-API connection. For pandas, we generally prefer using the SQLAlchemy engine instead.
    """
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the database directory and tables if they don't exist.

    Idempotent: safe to call multiple times. This is invoked on app startup so the
    first request won't fail with missing tables.
    """
    if not exists(dirname(DB_PATH)):
        os.makedirs(dirname(DB_PATH), exist_ok=True)
    print(f"Creating database directory at {dirname(DB_PATH)}")
    SQLModel.metadata.create_all(ENGINE)


def get_session() -> Session:
    """Create a SQLModel session bound to the global engine.

    Prefer using context managers (with get_session() as session) to ensure proper
    cleanup. In FastAPI, you can also wire this as a dependency if needed.
    """
    return Session(ENGINE)


def insert_transaction(tx: Union[Transaction, Mapping[str, Any]]) -> int:
    """Persist a transaction and return its primary key.

    Accepts either a Transaction model or a plain mapping. We keep id=None so SQLite
    autoincrements the primary key to avoid UNIQUE constraint failures.
    """
    if not isinstance(tx, Transaction):
        tx = Transaction(**tx)  # type: ignore[arg-type]
    with get_session() as session:
        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx.id or 0


def reset_database():
    """Delete and recreate the database schema.

    Disposes the engine first to release file handles on Windows/macOS, removes the
    DB file, and then recreates the schema. Handy in dev; secure or remove for prod.
    """
    ENGINE.dispose()
    if exists(DB_PATH):
        print(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)
    init_db()
