from typing import List

from .models import RetrievedSection


def determine_confidence(
    retrieved: List[RetrievedSection],
    refusal: bool,
) -> str:
    if refusal:
        return "very_low"
    if not retrieved:
        return "very_low"

    count = len(retrieved)
    conflicts = any(r.conflict_flag for r in retrieved)
    weak = any(r.coverage_weak for r in retrieved)

    if weak and count == 0:
        return "very_low"

    if conflicts or weak:
        return "low"

    if count >= 3:
        return "high"
    if 1 <= count <= 2:
        return "medium"

    return "very_low"
