"""
Airflow DAG: clean -> cluster -> join

Steps:
- clean: read CSV and load cleaned rows into SQLite 'transactions'
- cluster: read from SQLite and write clusters summary into 'transactions_clusters'
- join: read both tables and write a tiny joined summary 'transactions_joined'

Uses TaskFlow API. Paths configurable via env vars.
"""
from __future__ import annotations

import os
from datetime import datetime

from airflow.decorators import dag, task
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load sibling modules by file path (folder name has a hyphen, so not a valid package)
def _load_function(module_filename: str, func_name: str):
    path = os.path.join(BASE_DIR, module_filename)
    spec = importlib.util.spec_from_file_location(func_name + "_mod", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {module_filename}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, func_name)

run_clean = _load_function("nodes/clean.py", "run_clean")
run_cluster = _load_function("nodes/cluster.py", "run_cluster")
run_join = _load_function("nodes/join.py", "run_join")




# Inputs (override via env)
CSV_PATH = os.getenv(
    "TX_CSV_PATH",
    "/Users/julienlook/Documents/Coding/big-data-analytics/labs/data/transactions_data.csv",
)
SQLITE_DB = os.getenv(
    "TX_SQLITE_DB",
    "/Users/julienlook/Documents/Coding/big-data-analytics/labs/day3/data/transactions.db",
)
TX_JSON_PATH = os.getenv(
    "TX_JSON_PATH",
    "/Users/julienlook/Documents/Coding/big-data-analytics/labs/data/train_fraud_labels.json",
)


def ensure_dirs() -> None:
    os.makedirs(os.path.dirname(SQLITE_DB), exist_ok=True)

@dag(
    dag_id="transactions_ingest",
    description="Ingest transactions CSV into SQLite via Spark preprocessing",
    start_date=datetime(2025, 8, 1),
    schedule=None,
    catchup=False,
)
def transactions_ingest():
    @task
    def clean() -> None:
        ensure_dirs()
        run_clean(CSV_PATH, SQLITE_DB)

    # @task
    # def cluster() -> None:
    #     run_cluster(SQLITE_DB)

    @task
    def join() -> None:
        run_join(SQLITE_DB, TX_JSON_PATH)

    # clean() >> cluster() >> join()
    clean() >> join()


dag = transactions_ingest()
