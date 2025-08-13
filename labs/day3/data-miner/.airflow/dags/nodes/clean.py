"""
Clean step: read CSV with Spark, minimally clean/cast, and load into SQLite 'transactions'.

Each process owns its Spark session. This step reads from CSV and writes into SQLite
without requiring a JDBC driver (sqlite3 fallback).
"""
import os
from typing import List

from pyspark.sql.functions import *           # SQL functions (col, sum, avg, etc.)
from nodes.db import DB_COLUMNS, get_engine, ensure_transactions_table, write_df
from nodes.run_spark import get_spark



def run_clean(csv_path: str, sqlite_db_path: str) -> None:
	# Ensure DB directory exists
	db_dir = os.path.dirname(os.path.abspath(sqlite_db_path))
	if db_dir and not os.path.exists(db_dir):
		os.makedirs(db_dir, exist_ok=True)

	spark = get_spark()
	try:
		df = spark.read.csv(csv_path, header=True, inferSchema=True)

		# Minimal cleaning: cast numeric types and drop clearly invalid rows
		df = df.withColumn(
                    "amount", 
                    regexp_replace(col("amount"), "[\\$,]", "").cast("double")
                ).filter(col("amount") > 0).limit(1000)
		df = df.withColumn("currency", lit("usd"))
        # Ensure required columns exist; add nulls for missing
		for c in DB_COLUMNS:
			if c not in df.columns:
				df = df.withColumn(c, lit(None))

		# Avoid primary key collisions: set id to null so SQLite auto-assigns
	
		# df = df.withColumn("id", lit(None))

		# Reorder/select to match DB schema
		df = df.select(*DB_COLUMNS)

		# Write into SQLite via SQLModel engine
		engine = get_engine(sqlite_db_path)
		ensure_transactions_table(engine)
		write_df(engine, "transactions", df)
	finally:
		spark.stop()



__all__ = ["run_clean"]

