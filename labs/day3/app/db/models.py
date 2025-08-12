from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
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
    flagged_fraud: Optional[bool] = None
    is_fraud: Optional[bool] = None


class Decision(BaseModel):
    suspicious: bool
    reason: str
