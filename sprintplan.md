# Agile Sprint Plan for MVP

## Sprint 1: Core Backend & Data
- Set up repo, environments, and dependencies (FastAPI, Weaviate, GraphRAG).
- Write ingest script to load 5–20 crisis docs and create vectors in Weaviate.
- Build GraphRAG project graph from docs.
- Implement `/ask` FastAPI endpoint:
  - Integrate Weaviate for top-k passage retrieval.
  - Connect GraphRAG for multi-hop reasoning.
  - Return `{ answer, explanation_bullets, sources }`.
- Add basic unit tests for backend and endpoint.
- Document setup and usage in README.

## Sprint 2: Frontend & Integration
- Scaffold Next.js single-page UI:
  - Input box for questions.
  - Results panel for answer, steps, sources.
- Connect frontend to `/ask` API.
- Ensure accessibility and clear UX.
- Add fallback static example for demo reliability.
- Polish UI, error handling, and end-to-end flow.
- Add basic tests for frontend and integration.
- Finalize documentation and prepare demo script.

---

**Each sprint:**
- Define clear deliverables.
- Prioritize explainability, simplicity, and reproducibility.
- Review and adjust as needed.
