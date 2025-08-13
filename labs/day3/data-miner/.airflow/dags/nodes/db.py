from typing import Iterable

import pandas as pd
from sqlalchemy import text
from sqlmodel import create_engine


DB_COLUMNS: list[str] = [
	"id",
	"date",
	"client_id",
	"card_id",
	"amount",
	"currency",
	"use_chip",
	"merchant_id",
	"merchant_city",
	"merchant_state",
	"zip",
	"mcc",
	"description",
	"errors",
	"flagged_fraud",
	"is_fraud",
]


def get_engine(db_path: str):
	"""Create a SQLModel/SQLAlchemy engine for the SQLite DB."""
	return create_engine(f"sqlite:///{db_path}")


def ensure_transactions_table(engine) -> None:
	create_sql = text(
		"""
		CREATE TABLE IF NOT EXISTS transactions (
			id INTEGER PRIMARY KEY,
			date TEXT,
			client_id TEXT,
			card_id TEXT,
			amount REAL,
			currency TEXT,
			use_chip TEXT,
			merchant_id TEXT,
			merchant_city TEXT,
			merchant_state TEXT,
			zip TEXT,
			mcc INTEGER,
			description TEXT,
			errors TEXT,
			flagged_fraud BOOLEAN,
			is_fraud BOOLEAN
		)
		"""
	)
	with engine.begin() as conn:
		conn.execute(create_sql)


def write_df(engine, table: str, df) -> None:
	"""Batch-insert a Spark DataFrame using SQLAlchemy text parameters."""
	cols = df.columns
	col_list = ",".join(cols)
	placeholders = ",".join([f":{c}" for c in cols])
	insert_sql = text(f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})")
	with engine.begin() as conn:
		batch = []
		batch_size = 500
		for row in df.toLocalIterator():
			as_dict = row.asDict()
			params = {c: as_dict.get(c) for c in cols}
			batch.append(params)
			if len(batch) >= batch_size:
				conn.execute(insert_sql, batch)
				batch.clear()
		if batch:
			conn.execute(insert_sql, batch)


def read_sql_pdf(engine, query: str) -> pd.DataFrame:
	"""Read SQL into pandas using the given engine.
	Use a plain SQL string and the SQLAlchemy engine to keep pandas on the SQLAlchemy code path.
	"""
	return pd.read_sql_query(query, engine)
