# Copilot Instructions – Resilience-X (Hack Day)
Resilience-X helps answer “what/why/where” recovery questions from a tiny crisis corpus with explainability.

## Tech & scope (keep it simple)
- **Backend:** Python (FastAPI). Orchestrates Weaviate retrieval + GraphRAG multi-hop reasoning.
- **Frontend:** Next.js (NLWeb) single page with an input box and results panel (answer, steps, sources).
- **Vector DB:** Weaviate (localhost:8080).
- **Reasoning:** GraphRAG local project (small doc set).
- **Out of scope:** Heavy infra, advanced auth, complex data pipelines.

## Golden path (end-to-end)
1. Start Weaviate (Docker).
2. Ingest 5–20 short docs → create vectors (BYO embeddings).
3. Build a tiny GraphRAG project graph from the same docs.
4. Backend `/ask`:
   - Query Weaviate for top-k passages.
   - Run GraphRAG with the question + passages as context.
   - Return `{ answer, explanation_bullets, sources }`.
5. Frontend calls `/ask` and renders the three fields.

## Build & run commands
- Backend: `uv sync && uv run uvicorn services.api.main:app --reload --port 8000`
- Frontend: `npm ci --prefix apps/web && npm run dev --prefix apps/web`
- Weaviate (local): `docker compose up -d weaviate` (see `docker-compose.yml`)
- Ingest script: `bash scripts/ingest.sh`
- Demo script: `bash scripts/demo.sh`

## Repo structure (assume monorepo)
resilience-x/
apps/web/ # NLWeb UI (Next.js)
services/api/ # FastAPI /ask
rag/graphrag_project/ # GraphRAG config + pipeline
rag/data/ # 5–20 demo docs
vector/weaviate_bootstrap/ # schema + loader
scripts/ # ingest.sh, demo.sh
.github/

## Coding guidelines
- Prefer **clear, short** functions + docstrings; include types (py/ts).
- Always **return explainability**: 2–3 bullet “why” steps + source list.
- No secrets in code; use `.env` and `.gitignore`.
- Add a basic test for each new endpoint or utility.

## Resources Copilot can use
- `scripts/ingest.sh`, `scripts/demo.sh`
- `/services/api/clients/*` (GraphRAG + Weaviate small clients)
- `/apps/web/components/*` (simple, accessible UI components)

## What to avoid
- Large dependencies or long-running jobs.
- Heavy refactors during judging windows.
- Non-deterministic demos without a fallback static example.
