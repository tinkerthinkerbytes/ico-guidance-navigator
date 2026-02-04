from typing import Dict, List

from .models import RetrievedSection


def build_summary(retrieved: List[RetrievedSection]) -> str:
    if not retrieved:
        return "No relevant ICO guidance could be retrieved for this question."
    pieces = []
    for item in retrieved[:3]:
        para = item.section.paragraphs[0] if item.section.paragraphs else ""
        pieces.append(f"{item.section.title}: {para}")
    return " ".join(pieces)


def build_relevant_sections(retrieved: List[RetrievedSection]) -> List[Dict]:
    items: List[Dict] = []
    for item in retrieved:
        if not item.section.paragraphs:
            continue
        para_idx = item.matched_paragraphs[0] if item.matched_paragraphs else 0
        para_id = item.section.paragraph_ids[para_idx]
        why = f"Addresses the question in paragraph {para_id}: {item.section.paragraphs[para_idx]}"
        items.append({"title": item.section.title, "why_relevant": why})
    return items


def build_limitations(
    retrieved: List[RetrievedSection],
    refusal: bool,
) -> List[str]:
    limits = ["Static corpus limited to selected ICO guidance on one topic."]
    if refusal:
        limits.append("Request falls outside allowed advisory scope.")
    if not retrieved:
        limits.append("Retrieval returned no strong matches.")
    else:
        if any(r.coverage_weak for r in retrieved):
            limits.append("Retrieval signals are weak; relevance may be partial.")
        if any(r.conflict_flag for r in retrieved):
            limits.append("Guidance may be ambiguous or contain conflicting points.")
    return limits
