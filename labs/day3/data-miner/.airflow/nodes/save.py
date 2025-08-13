"""
Barebones saver: reads curated Parquet and writes to SQLite transactions table.

It tries Spark JDBC append if the SQLite JDBC driver is available, otherwise falls back
to inserting rows via sqlite3 using Python (slower but simple and dependency-free).
"""
import os
import sqlite3
from typing import Iterable

from pyspark.sql import SparkSession


def get_spark(app_name: str = "transactions_save") -> SparkSession:
	return (
		SparkSession.builder.appName(app_name)
		.config("spark.ui.showConsoleProgress", "false")
		.getOrCreate()
	)


def _jdbc_available() -> bool:
	# Caller can set SPARK_CLASSPATH to include the sqlite JDBC jar
	return bool(os.environ.get("SPARK_CLASSPATH"))


def save_parquet_to_sqlite(curated_parquet_path: str, sqlite_db_path: str, table: str = "transactions") -> None:
	spark = get_spark()
	try:
		df = spark.read.parquet(curated_parquet_path)

		if _jdbc_available():
			url = f"jdbc:sqlite:{sqlite_db_path}"
			(
				df.write.mode("append")
				.format("jdbc")
				.option("url", url)
				.option("dbtable", table)
				.save()
			)
			return

		# Fallback: collect in batches and insert via sqlite3
		cols = df.columns
		rows = df.toLocalIterator()  # stream rows
		_insert_rows_sqlite(sqlite_db_path, table, cols, rows)
	finally:
		spark.stop()


def _insert_rows_sqlite(db_path: str, table: str, cols: list[str], rows: Iterable) -> None:
	placeholders = ",".join(["?"] * len(cols))
	col_list = ",".join(cols)
	sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"
	conn = sqlite3.connect(db_path)
	try:
		cur = conn.cursor()
		# ensure table exists; let app create it typically, but be defensive
		# no-op if table already exists, relying on app's schema.
		# If missing, create a minimal compatible table.
		cur.execute(
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

		batch = []
		batch_size = 500
		for row in rows:
			values = [row[c] if c in row.asDict() else None for c in cols]
			batch.append(values)
			if len(batch) >= batch_size:
				cur.executemany(sql, batch)
				conn.commit()
				batch.clear()
		if batch:
			cur.executemany(sql, batch)
			conn.commit()
	finally:
		conn.close()


__all__ = ["save_parquet_to_sqlite"]

