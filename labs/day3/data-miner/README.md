# Data Miner – Airflow + PySpark pipeline

This folder contains the batch orchestration for Day 3. It runs a small ETL with PySpark under Airflow:

- clean: read CSV, normalize columns, write to SQLite `transactions.db`
- cluster: engineer per-customer features, run KMeans (k=3) with scaling, write counts to `transactions_clusters.db`
- join: load JSON labels and update `transactions.is_fraud`

## Quick init commands

Copy/paste this block to initialize Airflow locally in this folder:

```bash
export AIRFLOW_HOME="$PWD/.airflow" # defines root folder for DAGs
mkdir -p "$AIRFLOW_HOME/dags"       # DAG folder
airflow db migrate                   # register DAGs
airflow info | grep -E 'AIRFLOW_HOME|dags_folder' # check if DAG folder is recognised
airflow standalone                   # start airflow server & ui
```

## 1) Environment setup

Use a dedicated virtualenv for Airflow (Python 3.12):

```bash
cd labs/day3/data-miner
python3 -m venv .airflow-venv
source .airflow-venv/bin/activate
pip install -r requirements.txt
```

Initialize Airflow in a local folder inside this project:

```bash
export AIRFLOW_HOME="$PWD/.airflow"
mkdir -p "$AIRFLOW_HOME/dags"
airflow db migrate
airflow info | grep -E 'AIRFLOW_HOME|dags_folder'
```

Place/point DAGs:

- The DAG files live under `.airflow/dags` in this repo. Ensure Airflow sees that folder (output of the `airflow info` command above).

Start Airflow (webserver + scheduler in one):

```bash
airflow standalone
```

Airflow UI: http://127.0.0.1:8080

## 2) Configuration

Key environment variables (set in your shell or `.env` files as needed):

- TX_CSV_PATH – input CSV file path (default points to labs/day3/data/transactions_data.csv if present)
- TX_SQLITE_DB – main DB (e.g., `labs/day3/data/transactions.db`)
- TX_LABELS_JSON – labels JSON path for the join step (e.g., `labs/day3/labs/data/train_fraud_labels.json`)

The code uses `os.path` only; ensure the `labs/day3/data` directory exists and is writable.

## 3) Pipeline details

- clean task

  - Reads CSV with Spark
  - Cleans/casts amount, ensures schema columns, sets id to NULL to auto-increment in SQLite
  - Writes to `transactions` in `transactions.db` (via SQLModel engine)

- cluster task

  - Reads required columns from `transactions`
  - Aggregates features per client: total_spend, avg_transaction_amount, transaction_count, online_ratio, merchant_diversity
  - Assembles + scales features and runs KMeans (k=3, seed=42)
  - Writes distribution counts to `transactions_clusters` in `transactions_clusters.db`

- join task
  - Reads labels JSON and maps Yes/No → 1/0
  - Performs bulk UPDATE on `transactions.is_fraud` WHERE id matches

## 4) Run the DAG

In the Airflow UI, enable and trigger the `transactions_ingest` DAG.

Or via CLI:

```bash
airflow dags list
airflow dags trigger transactions_ingest
```

## 5) Outputs and verification

- labs/day3/data/transactions.db

  - Table: transactions
  - Verify row count and sums via Streamlit or sqlite browser

- labs/day3/data/transactions_clusters.db
  - Table: transactions_clusters (cluster, count)

Airflow task logs (for debugging):

```bash
ls -1 .airflow/logs/dag_id=transactions_ingest/
```

## 6) Troubleshooting

- DAG not visible:

  - Confirm `AIRFLOW_HOME` and `dags_folder` point to this repo’s `.airflow/dags`
  - Restart `airflow standalone`

- Import errors during DAG parse:

  - We defer heavy imports to task execution time; ensure Python path finds `.airflow/dags/nodes`

- SQLite lock/timeouts:

  - Re-run with fewer concurrent tasks; ensure no other process is writing while Airflow writes

- Pandas/SQLAlchemy errors:

  - We use SQLAlchemy engine + plain string queries; avoid passing `text(query)` directly to pandas

- Spark not found:
  - Ensure pyspark installed in `.airflow-venv` and available in PATH from that venv
