from typing import Optional

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: Optional[int] = Field(default=None)
    date: Optional[str] = None
    client_id: str
    card_id: Optional[str] = None
    amount: float
    use_chip: Optional[str] = None
    merchant_id: Optional[str] = None
    merchant_city: Optional[str] = None
    merchant_state: Optional[str] = None
    zip: Optional[str] = None
    mcc: Optional[int] = None
    errors: Optional[str] = None


class Decision(BaseModel):
    suspicious: bool
    reason: str
    score: float
    reason: str
    score: float
