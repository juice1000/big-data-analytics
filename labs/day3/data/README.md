# Data layer: local databases

This lab uses lightweight SQLite databases to keep the end-to-end flow simple, reproducible, and easy to inspect. You’ll find them under this folder:

- `transactions.db` — online events written by the FastAPI service
- `transactions_clusters.db` — batch analytics artifacts written by the Spark/ETL pipeline

## transactions.db (operational events)

Primary table: `transactions`

Key columns (from the SQLModel schema):

- `id`: INTEGER PRIMARY KEY
- `date`: TEXT (ISO-like string for simplicity in the lab)
- `client_id`: TEXT
- `card_id`: TEXT
- `amount`: REAL
- `currency`: TEXT
- `use_chip`: TEXT
- `merchant_id`: TEXT
- `merchant_city`: TEXT
- `merchant_state`: TEXT
- `zip`: TEXT
- `mcc`: INTEGER
- `description`: TEXT
- `errors`: TEXT (free-text notes; not critical to logic)
- `flagged_fraud`: BOOLEAN (0/1) — online decision from the API
- `is_fraud`: BOOLEAN (0/1, optional) — offline/ground-truth label (not used by the dashboard in this lab)

Notes:

- `id` could autoincrement, however we choose our own transaction id; usually inserts should not set `id` to avoid UNIQUE violations.
- `flagged_fraud` is produced at ingestion time (heuristics/LLM). `is_fraud` may be populated later by batch labeling; the current dashboard intentionally omits it from analysis.

## transactions_clusters.db (analytics artifacts)

This database holds compact summaries/results from the batch pipeline (Spark + KMeans). In this lab we use a simple table:

Table: `transactions_clusters`

- `cluster`: INTEGER — cluster id from KMeans
- `count`: INTEGER — number of customers in the cluster (or another aggregate)

Your pipeline may also write additional tables (e.g., per-customer features, centroids) as needed.

## Why SQLite?

- Zero-setup: No separate server to install or manage; works out-of-the-box across OSes.
- File-based: Easy to copy, back up, reset, and inspect during labs.
- Adequate for demos: Single-user, low-concurrency reads/writes are sufficient here.
- Great developer ergonomics: Query with standard SQL tools, pandas, or SQLModel.

Trade-offs:

- Concurrency limits: Single-writer; not ideal for many concurrent writers.
- Scaling constraints: No horizontal scaling or advanced HA/replication features.
- Feature set: Lacks some server-database features and extensions.

## How to scale from here

Choose the path that fits your needs; you can migrate incrementally.

- Relational (operational path):

  - Move to PostgreSQL or MySQL for transactional workloads.
  - Swap SQLModel’s connection string from SQLite to your server DB; keep the ORM models.
  - Add migrations (Alembic) for schema evolution and use connection pooling.
  - Centralize secrets and credentials (e.g., environment variables or a secrets manager).

- Analytics (batch/ML path):

  - Persist features/results in a warehouse or lakehouse (e.g., Parquet/Delta in object storage).
  - Use Spark/DBT/Lakehouse-native workflows for scalable transforms and governance.

- Streaming/real-time:

  - Introduce a message bus between the API and consumers.
  - Use a stream processor to enrich/score events; store hot aggregates in a cache, long-term data in a warehouse.

- Observability and governance:
  - Add metrics/logging and data quality checks.
  - Enforce access control, rotate keys, and restrict network paths.

## Operational tips

- Resetting: The FastAPI service exposes a reset endpoint for `transactions.db`; use cautiously.
- Backups: These are files; copying the `.db` files while the app is stopped is typically sufficient.
- Integrity: Keep writes simple and parameterized; avoid long-running transactions.
- Inspection: Use the `sqlite3` CLI, a SQLite GUI, or pandas `read_sql` to explore data.
