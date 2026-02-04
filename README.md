# ICO Guidance Navigator (Bounded RAG Demo)

Small, local, **bounded RAG** demo to help internal teams **navigate** (not interpret) ICO-style guidance by:

- retrieving relevant guidance sections from a **static local corpus**
- producing a **grounded, advisory-only** summary
- refusing inputs that ask for legal/compliance judgement or “what should we do” actions

## Quickstart

Requirements: **Python 3.10+** (stdlib-only; no external dependencies).

```bash
python3 -m venv .venv
source .venv/bin/activate

python3 -m app.cli "What does the guidance say about choosing and documenting a lawful basis?"
```

## Non-goals (hard constraints)

This project is **not**:

- legal advice
- a compliance decision engine
- a policy interpretation engine
- a production platform (no UI, auth, telemetry, scaling, etc.)

## Safety posture (high level)

- **Retrieval-first:** synthesis is grounded in retrieved sections only.
- **Deterministic refusal:** questions that require legal interpretation, compliance judgement, or action recommendations are refused.
- **Explicit limitations:** every response includes limitations; refusal returns `confidence="very_low"` and `relevant_sections=[]`.
- **No network fetch:** the corpus is local and static for this demo.

## Corpus (important)

The corpus in `app/corpus/` is:

- **static** (checked into the repo; no live fetching/scraping)
- **partial and illustrative** (intentionally small; not complete)
- written to resemble real guidance language for retrieval/synthesis evaluation

Do not treat the corpus as authoritative source text for real decisions.

## Run

```bash
python3 -m app.cli "your question"
```

## Run tests

```bash
python3 -m unittest -q
```

## Output contract

All outputs conform to the PRS JSON shape:

```json
{
  "summary": "string",
  "relevant_sections": [{"title": "string", "why_relevant": "string"}],
  "limitations": ["string"],
  "confidence": "very_low | low | medium | high"
}
```

## Repository layout

- `app/` — pipeline, retriever, refusal logic, output formatting
- `app/corpus/` — static local corpus used for retrieval
- `app/tests/` — unit tests for the pipeline contract and safety posture

## License

MIT — see `LICENSE`.
