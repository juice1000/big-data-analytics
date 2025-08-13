#!/usr/bin/env bash
set -e

# Minimal Airflow bootstrap: set AIRFLOW_HOME beside this script and start standalone.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export AIRFLOW_HOME="$DIR/.airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
mkdir -p "$AIRFLOW_HOME/dags"

# Activate virtual environment
source "$DIR/.airflow-venv/bin/activate"

# Loading env file (important to specify file paths)
[ -f "$DIR/.env" ] && set -a && . "$DIR/.env" && set +a

# Initialize metadata DB if first run
[ ! -f "$AIRFLOW_HOME/airflow.db" ] && airflow db migrate

# Execute Airflow standalone to launch the DAG
exec airflow standalone