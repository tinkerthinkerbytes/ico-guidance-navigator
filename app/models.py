from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Section:
    section_id: str
    title: str
    paragraphs: List[str]
    paragraph_ids: List[str]
    topic: str
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    embedding: Optional[List[float]] = None  # placeholder for future use
    bm25_blob: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class RetrievedSection:
    section: Section
    rank: int
    lexical_score: float
    embedding_score: float
    coverage_weak: bool
    conflict_flag: bool
    matched_paragraphs: List[int] = field(default_factory=list)
