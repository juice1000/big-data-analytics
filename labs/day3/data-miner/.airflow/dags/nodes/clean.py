"""Task node: CLEAN

Responsibility:
	- Read raw transactions CSV via Spark.
	- Minimal normalization (strip currency symbols, cast amount, enforce > 0).
	- Ensure all expected DB schema columns exist (add NULL placeholders if absent).
	- Select columns in canonical order and batch UPSERT into SQLite 'transactions'.

Design notes:
	- Spark session is created & stopped inside the task for isolation (simple for local lab).
	- Limit(1000) keeps resource usage low for demonstration; remove for full data.
	- Currency hard‑coded to 'usd' (lab simplification).
	- Primary key handling: id column should be NULL for fresh inserts; UPSERT logic
		in write_df allows reprocessing without duplicate key errors.
"""
import os
from typing import List

from pyspark.sql.functions import *           # SQL functions (col, sum, avg, etc.)
from nodes.db import DB_COLUMNS, get_engine, ensure_transactions_table, write_df
from nodes.run_spark import get_spark



def run_clean(csv_path: str, sqlite_db_path: str) -> None:
	# Ensure DB directory exists (idempotent).
	db_dir = os.path.dirname(os.path.abspath(sqlite_db_path))
	if db_dir and not os.path.exists(db_dir):
		os.makedirs(db_dir, exist_ok=True)

	spark = get_spark()
	try:
		df = spark.read.csv(csv_path, header=True, inferSchema=True)

		# Minimal cleaning: cast numeric part of 'amount' (strip $, commas) then keep positives.
		df = df.withColumn(
                    "amount", 
                    regexp_replace(col("amount"), "[\\$,]", "").cast("double")
                ).filter(col("amount") > 0).limit(1000)
		df = df.withColumn("currency", lit("usd"))
        # Ensure required columns exist; add nulls for missing
		for c in DB_COLUMNS:
			if c not in df.columns:
				df = df.withColumn(c, lit(None))

		# Primary key collisions avoided by NOT re-using source id when not stable.
		# Uncomment the next line to always force autoincrement on ingest.
		# df = df.withColumn("id", lit(None))

		# Reorder/select to match DB schema
		df = df.select(*DB_COLUMNS)

		# Write (UPSERT) into SQLite.
		engine = get_engine(sqlite_db_path)
		ensure_transactions_table(engine)
		write_df(engine, "transactions", df)
	finally:
		spark.stop()



__all__ = ["run_clean"]

