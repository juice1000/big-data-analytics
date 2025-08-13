"""DB helpers for task nodes (minimal, task-local abstraction).

Why not reuse API layer models? Keeping the Airflow side decoupled avoids tight
coupling / import path gymnastics; tasks only need lightweight batch insert + ensure schema.
"""

import pandas as pd
from sqlalchemy import text
from sqlmodel import create_engine


DB_COLUMNS: list[str] = [  # Canonical order for SELECT/INSERT alignment
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
	"""Create a SQLAlchemy engine for given SQLite file path."""
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
	"""Batch UPSERT Spark DataFrame rows into SQLite.

	Performs manual batching (size=500) to reduce transaction overhead.
	Uses SQLite ON CONFLICT(id) to update existing rows in place.
	"""
	cols = df.columns
	col_list = ",".join(cols)
	placeholders = ",".join([f":{c}" for c in cols])
	# UPSERT: if primary key 'id' exists, update remaining columns.
	update_assignments = ",".join([f"{c}=excluded.{c}" for c in cols if c != "id"])
	insert_sql = text(
		f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) ON CONFLICT(id) DO UPDATE SET {update_assignments}"
	)
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
	"""Run arbitrary SELECT and return pandas DataFrame (debug / ad-hoc use)."""
	return pd.read_sql_query(query, engine)
