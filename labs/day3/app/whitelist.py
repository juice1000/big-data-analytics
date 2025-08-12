from typing import Tuple

from storage import get_session


# Very simple amount-based deviation check using client's history
def amount_is_unusual(client_id: str, amount: float, factor: float = 3.0) -> Tuple[bool, float]:
    with get_session() as session:
        row = session.exec(
            "SELECT AVG(amount) as avg_amt, COUNT(*) as cnt FROM transactions WHERE client_id = :cid",
            {"cid": client_id},
        ).first()
        if not row:
            return False, 0.0
        avg_amt, cnt = row[0], row[1]
        if avg_amt is None or (cnt or 0) < 3:
            return False, 0.0
        avg = float(avg_amt)
        diff_ratio = abs(amount - avg) / (avg if avg else 1.0)
        return diff_ratio > factor, min(1.0, diff_ratio / factor)
