from db.storage import get_session
from sqlmodel import text

# Very simple amount-based deviation check using client's history
def amount_is_unusual(client_id: str, amount: float, factor: float = 3.0) -> bool | None:
    with get_session() as session:
        result = session.exec(
            text("SELECT AVG(amount) as avg_amt, COUNT(*) as cnt FROM transactions WHERE client_id = :cid").params(
                cid=client_id
            )
        )

        row = result.first()
        if not row:
            print("No data for client:", client_id)
            return None
        avg_amt, cnt = row[0], row[1]
        if avg_amt is None or (cnt or 0) < 3:
            print("Not enough data for client:", client_id)
            return None
        avg = float(avg_amt)
        diff_ratio = abs(amount - avg) / (avg if avg else 1.0)
        print(f"Client {client_id} - Amount: {amount}, Avg: {avg}, Diff Ratio: {diff_ratio:.2f}")
        return diff_ratio > factor



# Todo check for client id that exists