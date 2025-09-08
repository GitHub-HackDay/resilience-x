# Backlog: Epics and Sprints for MVP

## Epics

1. **Data Ingestion & Setup**
   - Repo/environment setup
   - Document ingestion and vectorization
   - GraphRAG project graph creation

2. **Backend API & Reasoning**
   - Implement `/ask` endpoint
   - Integrate Weaviate retrieval
   - Connect GraphRAG reasoning
   - Return answer, explanation bullets, sources

3. **Frontend UI & Integration**
   - Scaffold Next.js UI
   - Input box and results panel
   - Connect frontend to backend
   - Ensure accessibility and UX

4. **Testing & Explainability**
   - Add unit and integration tests
   - Polish explanation bullets and source tracing
   - Add fallback static example

5. **Demo & Documentation**
   - Finalize documentation
   - Prepare and validate demo script

---

## Sprints

### Sprint 1: Backend & Data
- Set up repo and environments
- Ingest crisis docs, create vectors in Weaviate
- Build GraphRAG project graph
- Implement `/ask` endpoint (Weaviate + GraphRAG)
- Basic backend tests
- Document setup/usage

### Sprint 2: Frontend & Integration
- Scaffold Next.js UI (input/results)
- Connect frontend to `/ask` API
- Accessibility and UX polish
- Add fallback static example
- End-to-end tests
- Finalize documentation and demo script
