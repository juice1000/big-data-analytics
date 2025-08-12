import re
from typing import Tuple

KEYWORDS = [r"urgent", r"verify", r"security", r"expires", r"immediate", r"update"]


def evaluate_text(description: str | None) -> Tuple[float, str]:
    if not description:
        return 0.0, "no description"
    text = description.lower()
    hits = sum(1 for k in KEYWORDS if re.search(k, text))
    if hits >= 2:
        return 0.8, "several fraud keywords"
    if hits == 1:
        return 0.4, "single fraud keyword"
    return 0.0, "no fraud keywords"
