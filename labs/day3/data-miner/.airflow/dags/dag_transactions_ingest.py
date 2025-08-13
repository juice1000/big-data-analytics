"""Airflow DAG definition for the batch pipeline (TaskFlow API).

High‑level goal:
    Orchestrate a simple analytics loop over card transactions: ingest + enrich
    (clean), derive customer clusters (cluster), then attach ground‑truth labels
    (join). Each task defers heavy imports / Spark startup to runtime to keep DAG
    parsing fast and resilient.

Execution order:
    clean  ->  join  ->  cluster

Tasks:
    clean   : Read raw CSV with Spark, normalize schema, upsert rows into SQLite 'transactions'.
    join    : Read labels JSON, bulk UPDATE transactions.is_fraud (id based).
    cluster : Build customer feature vectors from 'transactions' and write
                        cluster distribution counts to 'transactions_clusters'.

Environment variables (injected via .env or shell) so DAG code stays generic:
    TX_CSV_PATH     : path to source CSV
    TX_SQLITE_DB    : primary SQLite DB (stores transactions table)
    TX_CLUSTER_DB   : SQLite DB for cluster summary table
    TX_JSON_PATH    : labels JSON for join step

Why dynamic module loading here?
    The folder path contains hyphens / is outside a proper Python package; using
    importlib by file path guarantees Airflow can import even without modifying
    PYTHONPATH. This isolates node logic and keeps this DAG file concise.
"""
from __future__ import annotations

import os
from datetime import datetime

from airflow.decorators import dag, task
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper: load a function from a sibling Python file via absolute path.
# Avoids altering sys.path or creating ad‑hoc packages; keeps DAG portable.
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
CSV_PATH = os.getenv("TX_CSV_PATH")
SQLITE_DB = os.getenv("TX_SQLITE_DB")
CLUSTER_DB = os.getenv("TX_CLUSTER_DB")
TX_JSON_PATH = os.getenv("TX_JSON_PATH")

print(f"CSV_PATH: {CSV_PATH}")
print(f"SQLITE_DB: {SQLITE_DB}")
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
        """Ingest & normalize raw CSV into the transactions table.

        Idempotency: write_df uses UPSERT on primary key id, so re‑runs do not
        duplicate rows (unless the source file changed ids). Pre‑creates DB dir.
        """
        ensure_dirs()
        run_clean(CSV_PATH, SQLITE_DB)

    @task
    def join() -> None:
        """Attach offline labels to existing transactions (bulk UPDATE)."""
        run_join(SQLITE_DB, TX_JSON_PATH)

    @task
    def cluster() -> None:
        """Compute KMeans cluster distribution from updated transactions."""
        run_cluster(SQLITE_DB, CLUSTER_DB)

    # Execution graph: clean first (needs source CSV), then join (needs ids), then cluster (needs flags optional).
    clean() >> join() >> cluster()


dag = transactions_ingest()
