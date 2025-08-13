#!/usr/bin/env bash
# Minimal Airflow launcher for the lab:
# - Sets AIRFLOW_HOME beside this script
# - Loads optional .env (paths, config)
# - Activates local venv if present
# - Inits metadata DB on first run
# - Starts 'airflow standalone'
set -euo pipefail

# Resolve absolute directory of this script (handles invocation via symlink or elsewhere).
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Deterministic, repo-local Airflow home so all artifacts (db, logs, dags) live under versioned tree.
export AIRFLOW_HOME="$DIR/.airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES=False  # Skip example DAGs for clarity.
mkdir -p "$AIRFLOW_HOME/dags"

# Optional virtual environment activation: ensures 'airflow' and node dependencies resolve.
if [ -d "$DIR/.airflow-venv" ]; then
	# shellcheck disable=SC1091
	source "$DIR/.airflow-venv/bin/activate" || echo "(Warn) Failed to activate venv; continuing with system python"
else
	echo "(Info) No .airflow-venv directory found; assuming global environment has Airflow installed"
fi

# Load environment variables (e.g., TX_JSON_PATH). set -a exports any variable defined in .env.
if [ -f "$DIR/.env" ]; then
	set -a
	# shellcheck disable=SC1091
	. "$DIR/.env"
	set +a
else
	echo "(Info) No .env file found; proceeding without additional environment variables"
fi

echo "AIRFLOW_HOME=$AIRFLOW_HOME"

# Initialize metadata DB on first run; on subsequent runs it's a no-op.
if [ ! -f "$AIRFLOW_HOME/airflow.db" ]; then
	echo "Initializing Airflow metadata database..."
	airflow db init
else
	echo "Metadata database already present (skipping init)"
fi

echo "Starting Airflow (standalone)..."
exec airflow standalone