import os
import glob
import re
from typing import List

from .models import Section


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def split_paragraphs(text: str) -> List[str]:
    chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
    return chunks


def load_corpus(corpus_dir: str, topic: str = "lawful-basis-and-accountability") -> List[Section]:
    sections: List[Section] = []
    for path in sorted(glob.glob(os.path.join(corpus_dir, "*.md"))):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            continue
        lines = content.splitlines()
        title_line = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else os.path.basename(path)
        body = "\n".join(lines[1:]).strip()
        paragraphs = split_paragraphs(body)
        base_slug = slugify(os.path.splitext(os.path.basename(path))[0])
        paragraph_ids = [f"{base_slug}#p{i+1}" for i in range(len(paragraphs))]
        section = Section(
            section_id=base_slug,
            title=title_line,
            paragraphs=paragraphs,
            paragraph_ids=paragraph_ids,
            topic=topic,
            source_name=os.path.basename(path),
            source_url=None,
            bm25_blob=title_line + "\n" + "\n".join(paragraphs),
        )
        sections.append(section)
    return sections
