from math import atan2, cos, radians, sin, sqrt
from typing import Optional, Tuple

from storage import get_conn, last_user_location, last_user_stats


# Haversine distance between two lat/lon points (km)
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# Very simple amount-based deviation check using client's history


def amount_is_unusual(client_id: str, amount: float, factor: float = 3.0) -> Tuple[bool, float]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT AVG(amount), COUNT(*) FROM transactions WHERE client_id=?", (client_id,))
        row = cur.fetchone()
        if not row or row[0] is None or row[1] < 3:
            return False, 0.0
        avg = float(row[0])
        # Simple deviation score
        diff_ratio = abs(amount - avg) / (avg if avg else 1.0)
        return diff_ratio > factor, min(1.0, diff_ratio / factor)


def location_is_unusual(
    client_id: str, lat: Optional[float], lon: Optional[float], km_threshold: float = 500.0
) -> Tuple[bool, float]:
    if lat is None or lon is None:
        return False, 0.0
    last_loc = last_user_location(client_id)
    if not last_loc:
        return False, 0.0
    last_lat, last_lon = last_loc
    dist = haversine_km(last_lat, last_lon, lat, lon)
    return dist > km_threshold, min(1.0, dist / km_threshold)
    return dist > km_threshold, min(1.0, dist / km_threshold)
