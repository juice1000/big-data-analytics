"""
Barebones loader: reads the source CSV into a Spark DataFrame and writes it as raw Parquet.

This module is intentionally minimal. It creates its own SparkSession, reads the CSV,
and persists a Parquet dataset for downstream steps (preprocess/save) to consume.
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
	spark.stop()

def load_from_csv(spark: SparkSession, csv_path: str) -> DataFrame:
	return spark.read.csv(csv_path, header=True, inferSchema=True)

def write_to_sql(df: DataFrame, db_path: str, table_name: str) -> None:
	conn = sqlite3.connect(db_path)
	try:
		df.write.jdbc(url=f"jdbc:sqlite:{db_path}", table=table_name, mode="overwrite")
	finally:
		conn.close()
