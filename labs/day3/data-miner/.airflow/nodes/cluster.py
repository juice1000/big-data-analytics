"""
Cluster step: read from SQLite 'transactions' into Spark, perform a simple clustering (KMeans) on amount,
write the clustered assignments back to SQLite table 'transactions_clusters'.

Focus: minimal and robust.
"""
import sqlite3

from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_spark(app_name: str = "tx_cluster") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )


def run_cluster(sqlite_db_path: str, k: int = 3) -> None:
    spark = get_spark()
    try:
        # Load via JDBC if available; fallback to pandas->spark via sqlite3
        df = _read_transactions(spark, sqlite_db_path)
        # Minimal numeric feature set
        if "amount" not in df.columns:
            return
        numeric = df.select("amount").na.fill(0.0)
        vec = VectorAssembler(inputCols=["amount"], outputCol="features").transform(numeric)
        km = KMeans(k=k, seed=42, featuresCol="features", predictionCol="cluster")
        model = km.fit(vec)
        clustered = model.transform(vec).select("amount", "cluster")

        # Save clusters count per cluster for quick insights
        out = clustered.groupBy("cluster").agg(F.count("*").alias("count"))
        _write_clusters_to_sqlite(out, sqlite_db_path)
    finally:
        spark.stop()


def _read_transactions(spark: SparkSession, db_path: str):
    # Cheap and cheerful: use sqlite3 -> pandas -> spark to avoid JDBC jar
    import pandas as pd

    conn = sqlite3.connect(db_path)
    try:
        pdf = pd.read_sql_query("SELECT amount FROM transactions WHERE amount IS NOT NULL", conn)
    finally:
        conn.close()
    return spark.createDataFrame(pdf)


def _write_clusters_to_sqlite(df, db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions_clusters (
                cluster INTEGER,
                count INTEGER
            )
            """
        )
        cur.execute("DELETE FROM transactions_clusters")
        rows = [(int(r["cluster"]), int(r["count"])) for r in df.collect()]
        cur.executemany("INSERT INTO transactions_clusters (cluster, count) VALUES (?, ?)", rows)
        conn.commit()
    finally:
        conn.close()


__all__ = ["run_cluster"]
