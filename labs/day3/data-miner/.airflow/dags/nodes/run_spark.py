"""Spark session utilities.

Currently only supplies a configured local SparkSession factory (get_spark) used by
task nodes. Consolidated here so tuning (memory, shuffle partitions, logging) can be
done in a single place if pipeline grows.
"""
from pathlib import Path
from typing import Optional

from pyspark.sql import DataFrame, SparkSession


def get_spark(app_name: str = "transactions_loader") -> SparkSession:
	return (
		SparkSession.builder.appName(app_name)
		.config("spark.ui.showConsoleProgress", "false")
		.config("spark.driver.host", "127.0.0.1")  # Force localhost binding to avoid network issues
		.config("spark.driver.bindAddress", "127.0.0.1")  # Explicit bind address for driver
		.getOrCreate()
	)

def stop_spark(spark: SparkSession) -> None:
	"""Explicit Spark shutdown (not always needed when process exits)."""
	spark.stop()

def load_from_csv(spark: SparkSession, csv_path: str) -> DataFrame:
	"""Convenience read (header + schema inference)."""
	return spark.read.csv(csv_path, header=True, inferSchema=True)

def write_to_sql(df: DataFrame, db_path: str, table_name: str) -> None:
	"""(Unused) Example of writing via JDBC if needed later."""
	import sqlite3
	conn = sqlite3.connect(db_path)
	try:
		df.write.jdbc(url=f"jdbc:sqlite:{db_path}", table=table_name, mode="overwrite")
	finally:
		conn.close()
