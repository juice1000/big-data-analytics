# Data Miner – Airflow + PySpark pipeline

Small batch ETL orchestrated by Apache Airflow (standalone mode) to support Day 3:

| Task    | Purpose                                                                                |
| ------- | -------------------------------------------------------------------------------------- |
| clean   | Read CSV, normalize schema, insert / upsert rows into `transactions.db`                |
| join    | Load JSON labels, bulk update `transactions.is_fraud`                                  |
| cluster | Feature engineer per client + KMeans (k=3), write counts to `transactions_clusters.db` |

Airflow UI runs at: http://127.0.0.1:8080

## Quick start

```bash
cd labs/day3/data-miner
python3 -m venv .airflow-venv          # create isolated env just for Airflow & Spark deps
source .airflow-venv/bin/activate      # activate it (needed every new shell)
pip install -r requirements.txt        # install orchestrator + PySpark deps
./run_airflow.sh                       # sets AIRFLOW_HOME locally and launches standalone
```

Then open the web UI above, enable the `transactions_ingest` DAG, and trigger it.

## Why this flow?

- Separate virtualenv: keeps heavier Airflow/Spark pins out of the rest of the project.
- Local `AIRFLOW_HOME`: all metadata DB, logs, and DAGs stay inside the repo (`.airflow/`). Easy cleanup.
- Single launcher (`run_airflow.sh`): removes manual export steps; guarantees DAGs live where the scheduler scans.
- Simplicity: minimal moving parts for a learning lab (no external metastore / executor).

## Configuration (optional overrides)

Set in `.env` (auto‑loaded by the script) or your shell:

- `TX_CSV_PATH` – input CSV (defaults to `labs/day3/data/transactions_data.csv` if present)
- `TX_SQLITE_DB` – path to main SQLite DB (e.g. `labs/day3/data/transactions.db`)
- `TX_LABELS_JSON` – JSON labels file for `join` task

If unset, tasks attempt sensible defaults relative to the repo.

## Outputs

- `labs/day3/data/transactions.db` – table `transactions`
- `labs/day3/data/transactions_clusters.db` – table `transactions_clusters` (cluster, count)

Inspect via SQLite client or the monitoring Streamlit app in `labs/day3/monitoring`.

## Troubleshooting (trimmed)

- DAG missing: confirm `.airflow/dags` contains the DAG files; restart script.
- Spark import error: ensure `pyspark` installed in the activated `.airflow-venv`.
- SQLite lock: re‑run with fewer parallel tasks; standalone mode usually avoids heavy contention.

Everything else: check task logs in `.airflow/logs/` from the UI or filesystem.
