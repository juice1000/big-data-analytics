"""
Cluster step: read from SQLite 'transactions' via SQLModel engine, perform simple KMeans on amount,
write the cluster counts back to SQLite table 'transactions_clusters'.

Focus: minimal and robust.
"""

from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from nodes.db import get_engine, read_sql_pdf


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
    engine = get_engine(db_path)
    pdf = read_sql_pdf(engine, "SELECT amount FROM transactions WHERE amount IS NOT NULL")
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
