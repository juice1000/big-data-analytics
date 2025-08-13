"""
Cluster step: build customer-level features and run KMeans clustering with scaling.
Writes cluster distribution to SQLite table 'transactions_clusters'.
"""

import sqlite3
from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from sqlalchemy import text
from nodes.db import get_engine
from nodes.run_spark import get_spark


def run_cluster(sqlite_db_path: str, cluster_db_path: str) -> None:
    spark = get_spark()
    try:
        # Load transactions with necessary columns
        df = _read_transactions(spark, sqlite_db_path)

        # Build customer-level features
        print("Preparing customer features for clustering...")
        grouped = (
            df.groupBy("client_id")
            .agg(
                F.sum("amount").alias("total_spend"),
                F.avg("amount").alias("avg_transaction_amount"),
                F.count("*").alias("transaction_count"),
                F.sum(F.when(F.lower(F.coalesce(F.col("use_chip"), F.lit(""))) == F.lit("online"), F.lit(1)).otherwise(F.lit(0))).alias("online_count"),
                F.countDistinct("merchant_id").alias("merchant_diversity"),
            )
        )
        customer_features = grouped.withColumn(
            "online_ratio",
            F.col("online_count") / F.when(F.col("transaction_count") == 0, F.lit(1)).otherwise(F.col("transaction_count"))
        ).drop("online_count")

        feature_cols = [
            "total_spend",
            "avg_transaction_amount",
            "transaction_count",
            "online_ratio",
            "merchant_diversity",
        ]

        # Defensive fill for missing columns
        for c in feature_cols:
            if c not in customer_features.columns:
                customer_features = customer_features.withColumn(c, F.lit(0.0))

        print(f"Using {customer_features.count():,} customers for clustering")

        customer_features_clean = customer_features.select("client_id", *feature_cols).na.fill(0.0)

        # ML Pipeline: assemble -> scale -> kmeans
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
        scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
        kmeans = KMeans(featuresCol="scaledFeatures", k=3, seed=42) # We can also tune the number of clusters using the elbow method
        pipeline = Pipeline(stages=[assembler, scaler, kmeans])

        print("Training K-means model...")
        model = pipeline.fit(customer_features_clean)
        predictions = model.transform(customer_features_clean)
        print("K-means clustering completed!")

        # Cluster distribution
        out = predictions.groupBy("prediction").count().orderBy("prediction").withColumnRenamed("prediction", "cluster")
        out = out.select("cluster", "count")
        _write_clusters_to_sqlite(out, cluster_db_path)
    finally:
        spark.stop()


def _read_transactions(spark: SparkSession, db_path: str):
    engine = get_engine(db_path)
    query = (
        "SELECT client_id, amount, use_chip, merchant_id "
        "FROM transactions WHERE amount IS NOT NULL"
    )
    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()

    if not rows:
        # Return empty DF with expected schema
        return spark.createDataFrame([], schema="client_id string, amount double, use_chip string, merchant_id string")

    data = [(r[0], float(r[1]) if r[1] is not None else None, r[2], r[3]) for r in rows]
    return spark.createDataFrame(data, schema=["client_id", "amount", "use_chip", "merchant_id"])


def _write_clusters_to_sqlite(df, db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    print("were're here")
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
