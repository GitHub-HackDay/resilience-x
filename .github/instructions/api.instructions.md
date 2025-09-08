---
applyTo: "services/api/**/*.py"
---

# API Rules (FastAPI)
- Expose only `/ask` (POST) with `{ question: string }`.
- Return JSON: `{ answer: string, explanation_bullets: string[], sources: string[] }`.
- Add `pydantic` models; include docstrings and type hints.
- Time out upstream calls quickly; return a friendly fallback if GraphRAG is unavailable.
- Log errors with minimal PII; never log secrets.
