"""
Clean step: read CSV with Spark, minimally clean/cast, and load into SQLite 'transactions'.

Each process owns its Spark session. This step reads from CSV and writes into SQLite
without requiring a JDBC driver (sqlite3 fallback).
"""
import os
import sqlite3
from typing import List

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from ..nodes.db import DB_COLUMNS
from run_spark import get_spark



def run_clean(csv_path: str, sqlite_db_path: str) -> None:
	# Ensure DB directory exists
	db_dir = os.path.dirname(os.path.abspath(sqlite_db_path))
	if db_dir and not os.path.exists(db_dir):
		os.makedirs(db_dir, exist_ok=True)

	spark = get_spark()
	try:
		df = spark.read.csv(csv_path, header=True, inferSchema=True)

		# Minimal cleaning: cast numeric types and drop clearly invalid rows
		sample_df = sample_df.withColumn(
                    "amount_numeric", 
                    regexp_replace(col("amount"), "[\\$,]", "").cast("double")
                ).filter(col("amount_numeric") > 0)
		
        # Ensure required columns exist; add nulls for missing
		for c in DB_COLUMNS:
			if c not in df.columns:
				df = df.withColumn(c, F.lit(None))

		# Avoid primary key collisions: set id to null so SQLite auto-assigns
		df = df.withColumn("id", F.lit(None))

		# Reorder/select to match DB schema
		df = df.select(*DB_COLUMNS)

		# Write into SQLite
		_write_df_to_sqlite(df, sqlite_db_path, "transactions")
	finally:
		spark.stop()


def _write_df_to_sqlite(df, db_path: str, table: str) -> None:
	conn = sqlite3.connect(db_path)
	try:
		cur = conn.cursor()
		# Create table if not exists (aligned with app schema)
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

		cols = df.columns
		placeholders = ",".join(["?"] * len(cols))
		col_list = ",".join(cols)
		sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

		batch = []
		batch_size = 500
		for row in df.toLocalIterator():
			as_dict = row.asDict()
			values = [as_dict.get(c) for c in cols]
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


__all__ = ["run_clean"]

