"""
Streamlit dashboard for observing transactions and cluster summaries.

Why these choices:
- We use SQLModel Sessions and the shared Transaction model to keep the dashboard
  aligned with the API's schema. This reduces drift and avoids raw string SQL where
  a typed query improves safety.
- We add the app/ folder to sys.path to import the SQLModel definitions defined by
  the FastAPI service. In a real project you'd package the models, but for a lab this
  is a pragmatic way to share types.
- We keep paths relative to this file so you can run it from anywhere without having
  to cd first. Both transactions.db (events) and transactions_clusters.db (analytics)
  live under ../data relative to this script.


HOW A STREAMLIT APP RUNS (quick primer):
- A Streamlit app is just a Python script executed top-to-bottom to render a page.
- Any user interaction (changing a widget, pressing a button) triggers a rerun of the
    entire script. Values read from widgets (e.g., st.checkbox) are recomputed on rerun.
- To avoid re-computing expensive work across reruns, use caching decorators like
    st.cache_data (for data frames/results) or st.cache_resource (for clients/connections).
- If you need to persist UI state across reruns (counters, flags), store it in
    st.session_state; local variables reset on each rerun.
- There's no explicit routing like in FastAPI; you compose the page by writing Python
    that emits UI components (st.title, st.metric, st.dataframe, etc.).
"""

import os
import sys
import pandas as pd
from sqlalchemy import func, text
from sqlmodel import Session, create_engine, select

import streamlit as st

# Always work relative to this script's directory so local runs are consistent
# regardless of the current working directory in the terminal. This prevents
# brittle code that depends on 'where you launched streamlit from'.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join("..", "data", "transactions.db")
CLUSTERS_DB_PATH = os.path.join("..", "data", "transactions_clusters.db")

# Allow importing the shared models from the sibling FastAPI app (labs/day3/app).
# This keeps ORM models centralized. In production, prefer installing a shared package
# rather than tinkering with sys.path.
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app")
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)
from db.models import Transaction


def get_engine():
    """Create an engine for the transactions DB if it exists."""
    if not os.path.exists(DB_PATH):
        return None
    # For heavier Streamlit concurrency you might need connect_args like
    # {"check_same_thread": False}. For this lab's read-only usage the default is fine.
    return create_engine(f"sqlite:///{DB_PATH}")


def get_session():
    """Return a Session for the transactions DB."""
    engine = get_engine()
    if engine is None:
        return None
    return Session(engine)


def get_clusters_session():
    """Return a Session for the clusters DB.

    We haven't defined ORM models for cluster summaries in this lab, so we use text()
    queries below. If this grows, define a SQLModel and switch to typed selects.
    """
    if not os.path.exists(CLUSTERS_DB_PATH):
        return None
    engine = create_engine(f"sqlite:///{CLUSTERS_DB_PATH}")
    return Session(engine)


st.set_page_config(page_title="Transaction Monitoring", layout="wide")
st.title("Transaction Monitoring")


def load_metrics():
    """Aggregate KPIs for the header metrics.

    Notes:
    - We use typed selects with SQLModel for count/sum to avoid string SQL.
    - SQLite stores booleans as integers (0/1); comparisons to True work with SQLAlchemy.
    - If the DB doesn't exist yet, we show a friendly empty state.
    """
    session = get_session()
    if session is None:
        return None
    try:
        total_tx = int(session.exec(select(func.count()).select_from(Transaction)).one() or 0)
        if total_tx == 0:
            return {"total_tx": 0, "total_amount": 0.0, "potential_fraud": 0, "is_fraud_count": 0}

        # SUM can return NULL if there are no rows; coalesce to 0 to keep display tidy.
        total_amount = float(session.exec(select(func.coalesce(func.sum(Transaction.amount), 0))).one() or 0.0)

        # flagged_fraud is the online signal written by the API.
        potential_fraud = int(session.exec(select(func.count()).where(Transaction.flagged_fraud == True)).one() or 0)

        return {
            "total_tx": total_tx,
            "total_amount": total_amount,
            "potential_fraud": potential_fraud,
        }
    except Exception:
        # If table doesn't exist yet or any other issue, treat as no data
        return None


data = load_metrics()
# If there's no database yet or zero rows, don't error—show a friendly hint.
if not data or data["total_tx"] == 0:
    st.info("No data available yet. The dashboard will populate as transactions arrive.")
else:
    # Top KPI strip. We keep it to four metrics for quick scanning.
    col1, col2, col3 = st.columns(3)
    col1.metric("Transactions", f"{data['total_tx']:,}")
    col2.metric("Total Amount", f"{data['total_amount']:,.2f}")
    col3.metric("Potential Fraud", f"{data['potential_fraud']:,}")
    # Caption clarifies metric sources (online flags only).
    st.caption("Potential fraud uses flagged_fraud from the API.")

    # Recent transactions table (20 rows)
    def load_recent_transactions(limit: int = 20, only_flagged: bool = False):
        """Fetch the most recent transactions with optional filters.

        We keep an explicit column list to produce a stable table regardless of model changes.
        SQLModel instances are converted to dicts (Pydantic v2 exposes model_dump()).
        Consider caching (st.cache_data) if the dataset grows; for small SQLite tables
        and frequent updates, direct reads keep freshness without cache invalidation.
        """
        session = get_session()
        if session is None:
            return None
        try:
            # Build the base query and apply filters if toggles are set.
            query = select(Transaction)
            if only_flagged:
                query = query.where(Transaction.flagged_fraud == True)
            # is_fraud omitted by request; only flagged_fraud filter remains.
            query = query.order_by(Transaction.id.desc()).limit(limit)
            results = session.exec(query).all()

            # Normalize SQLModel instances to dicts for DataFrame
            def _to_dict(obj):
                if hasattr(obj, "model_dump"):
                    return obj.model_dump()
                if hasattr(obj, "dict"):
                    return obj.dict()
                return obj.__dict__

            rows = []
            cols = [
                "id",
                "date",
                "client_id",
                "card_id",
                "amount",
                "currency",
                "merchant_city",
                "mcc",
                "description",
                "flagged_fraud",
            ]
            for tx in results:
                d = _to_dict(tx)
                rows.append({k: d.get(k) for k in cols})
            return pd.DataFrame(rows)
        except Exception:
            return None

    # Filters control server-side queries instead of client-side filtering to avoid
    # sending unnecessary data to the browser.
    only_flagged = st.checkbox("Show only flagged_fraud = 1", value=False)
    recent_df = load_recent_transactions(20, only_flagged=only_flagged)
    st.subheader("Recent transactions (latest 20)")
    # Provide a readable empty state instead of an empty table when there's no data.
    if recent_df is None or recent_df.empty:
        st.write("No recent transactions to display.")
    else:
        # Use a fixed height to keep the page from growing unbounded with long tables.
        st.dataframe(recent_df, use_container_width=True, height=400)

    # Clusters table from transactions_clusters.db
    st.subheader("Clusters (transactions_clusters.db)")
    clusters_session = get_clusters_session()
    if clusters_session is None:
        st.write("No clusters database found yet.")
    else:
        try:
            # No ORM model for cluster summaries; use a text() query and map rows to dicts.
            # This table is written by the batch pipeline. If the pipeline hasn't run yet
            # or schema differs, the dashboard degrades gracefully.
            result = clusters_session.exec(text("SELECT * FROM transactions_clusters ORDER BY cluster ASC"))
            rows = [dict(r) for r in result.mappings().all()]
            clusters_df = pd.DataFrame(rows)
            if clusters_df.empty:
                st.write("No cluster data to display.")
            else:
                st.dataframe(clusters_df, use_container_width=True, height=300)
        except Exception as e:
            st.write(f"Failed to read clusters table: {e}")
