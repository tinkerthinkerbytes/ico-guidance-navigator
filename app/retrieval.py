import math
import re
from collections import Counter, defaultdict
from typing import List, Tuple

from .models import Section, RetrievedSection


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


# Minimal stopwords for coverage checks. This is not used for ranking; only to
# detect weak/out-of-corpus retrieval and downgrade confidence accordingly.
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "about",
    "before",
    "be",
    "by",
    "can",
    "could",
    "data",
    "do",
    "does",
    "for",
    "from",
    "guidance",
    "how",
    "i",
    "ico",
    "if",
    "in",
    "include",
    "is",
    "it",
    "information",
    "need",
    "of",
    "on",
    "or",
    "our",
    "personal",
    "processing",
    "say",
    "says",
    "should",
    "that",
    "the",
    "their",
    "to",
    "under",
    "we",
    "what",
    "when",
    "where",
    "which",
    "who",
    "would",
    "you",
}


def content_terms(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in STOPWORDS and len(t) >= 3]


class BM25Retriever:
    def __init__(self, sections: List[Section], k1: float = 1.5, b: float = 0.75):
        self.sections = sections
        self.k1 = k1
        self.b = b
        self.doc_tokens = [tokenize(s.bm25_blob or "") for s in sections]
        self.doc_term_sets = [set(content_terms(toks)) for toks in self.doc_tokens]
        self.doc_lengths = [len(toks) for toks in self.doc_tokens]
        self.avg_len = sum(self.doc_lengths) / len(self.doc_lengths) if self.doc_lengths else 0
        self.df = defaultdict(int)
        for toks in self.doc_tokens:
            for term in set(toks):
                self.df[term] += 1
        self.N = len(sections)

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_tokens = tokenize(query)
        q_counts = Counter(q_tokens)
        scores = []
        for idx, toks in enumerate(self.doc_tokens):
            doc_tf = Counter(toks)
            doc_len = self.doc_lengths[idx] or 1
            score = 0.0
            for term, qf in q_counts.items():
                if term not in doc_tf:
                    continue
                df = self.df.get(term, 0.5)
                idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
                tf = doc_tf[term]
                denom = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_len or 1))
                score += idf * (tf * (self.k1 + 1) / denom) * qf
            scores.append((idx, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def retrieve(self, query: str, top_k: int = 5) -> List[RetrievedSection]:
        scored = self.score(query)
        results: List[RetrievedSection] = []
        if not scored:
            return results
        max_score = scored[0][1] if scored else 0.0
        q_terms = set(content_terms(tokenize(query)))
        coverage_threshold = 0.1  # implementation-defined, used only for downgrades
        for rank, (idx, score) in enumerate(scored[:top_k], start=1):
            # Coverage signals are downgrade-only; they do not affect ranking.
            overlap_weak = False
            if q_terms:
                overlap_weak = len(q_terms & self.doc_term_sets[idx]) == 0
            coverage_weak = score < coverage_threshold or max_score < coverage_threshold or overlap_weak
            results.append(
                RetrievedSection(
                    section=self.sections[idx],
                    rank=rank,
                    lexical_score=score,
                    embedding_score=0.0,
                    coverage_weak=coverage_weak,
                    conflict_flag=False,
                    matched_paragraphs=[],
                )
            )
        return results
