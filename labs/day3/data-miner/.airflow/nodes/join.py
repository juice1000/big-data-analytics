"""
Join step: read from SQLite 'transactions' and 'transactions_clusters' and produce a tiny joined view.
Writes result into 'transactions_joined' table for downstream use.
"""
import sqlite3

import pandas as pd
from pyspark.sql import SparkSession


def get_spark(app_name: str = "tx_join") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )


def run_join(sqlite_db_path: str) -> None:
    spark = get_spark()
    try:
        conn = sqlite3.connect(sqlite_db_path)
        try:
            t_pdf = pd.read_sql_query("SELECT amount FROM transactions", conn)
            c_pdf = pd.read_sql_query("SELECT cluster, count FROM transactions_clusters", conn)
        finally:
            conn.close()

        t_df = spark.createDataFrame(t_pdf)
        c_df = spark.createDataFrame(c_pdf)

        # Example: compute avg amount and attach cluster summary (cartesian-free via collecting small c_df)
        avg_amount = t_df.selectExpr("avg(amount) as avg_amount").collect()[0]["avg_amount"]
        # store a tiny one-row table with the avg and clusters total rows
        clusters_total = c_df.selectExpr("sum(count) as total_clustered").collect()[0]["total_clustered"]

        out_pdf = pd.DataFrame({
            "avg_amount": [avg_amount],
            "total_clustered": [clusters_total],
        })

        conn = sqlite3.connect(sqlite_db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions_joined (
                    avg_amount REAL,
                    total_clustered INTEGER
                )
                """
            )
            cur.execute("DELETE FROM transactions_joined")
            cur.executemany(
                "INSERT INTO transactions_joined (avg_amount, total_clustered) VALUES (?, ?)",
                list(out_pdf.itertuples(index=False, name=None)),
            )
            conn.commit()
        finally:
            conn.close()
    finally:
        spark.stop()


__all__ = ["run_join"]
