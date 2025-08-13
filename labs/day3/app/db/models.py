from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    """Domain entity for a card transaction and the table schema.

    Notes on fields:
    - id: autoincrement primary key (keep default None before inserts to avoid UNIQUE errors)
    - flagged_fraud: what the online decisioning engine flags in real time (our output)
    - is_fraud: the ground-truth label (from offline labeling/joins), may be NULL at ingest time
    Keeping both allows monitoring precision/recall downstream.
    """

    __tablename__ = "transactions"

    # Primary key is optional on the model so SQLite can autogenerate it.
    id: Optional[int] = Field(default=None, primary_key=True)
    # Keep dates as strings for simplicity in the lab (no tz headaches).
    date: Optional[str] = None
    client_id: str
    card_id: Optional[str] = None
    amount: float
    currency: Optional[str] = None
    use_chip: Optional[str] = None
    merchant_id: Optional[str] = None
    merchant_city: Optional[str] = None
    merchant_state: Optional[str] = None
    zip: Optional[str] = None
    mcc: Optional[int] = None
    description: Optional[str] = None
    errors: Optional[str] = None
    # Online flag (from our evaluator) vs offline truth (from labels/joins)
    flagged_fraud: Optional[bool] = None
    is_fraud: Optional[bool] = None


class Decision(BaseModel):
    """Minimal API response returning the decision and why.

    This shape is intentionally small to demonstrate explainability and
    keep clients decoupled from the full Transaction schema.
    """

    suspicious: bool
    reason: str
