from typing import Dict
import re


REFUSAL_PATTERNS = [
    r"\bis this lawful\b",
    # Lawfulness / legality judgments (avoid matching "lawful basis" guidance questions).
    r"\b(is|are)\b.{0,80}\b(lawful|legal)\b(?!\s+basis)",
    r"\b(lawful|legal)\b.{0,80}\bunder\b.{0,40}\b(uk\s*)?gdpr\b(?!\s+basis)",
    r"\bunder\b.{0,40}\b(uk\s*)?gdpr\b.{0,80}\b(lawful|legal|compliant)\b(?!\s+basis)",
    r"\bare we compliant\b",
    r"\bcompliant if\b",
    r"\b(would|will)\b.{0,40}\b(be\s+)?compliant\b",
    r"\bwhat should we do\b",
    r"\bshould we\b.*compliance",
    r"\bwhat do we need to do\b.*\bcomply\b",
    r"\b(step[- ]by[- ]step|step by step)\b.{0,80}\b(plan|guide)\b",
    r"\b(plan|guide)\b.{0,80}\b(become|be)\b.{0,40}\bcompliant\b",
    r"\bgive legal advice\b",
    r"\blegal advice\b",
    r"\bcompliance decision\b",
    r"\bcan we proceed\b",
]


def should_refuse(question: str) -> bool:
    q = question.lower()
    for pat in REFUSAL_PATTERNS:
        if re.search(pat, q):
            return True
    return False


def refusal_response(reason: str) -> Dict:
    return {
        "summary": reason,
        "relevant_sections": [],
        "limitations": [reason],
        "confidence": "very_low",
    }
