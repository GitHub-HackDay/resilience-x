# Copilot Coding Agent – Resilience-X

## Tasks you may perform
- Create/modify the `/ask` endpoint and small clients for Weaviate + GraphRAG.
- Generate minimal unit/integration tests.
- Update README sections (“Golden Path”, run commands).
- Add small accessibility tweaks in the web app.

## Do before opening a PR
1) Run setup:
   - `docker compose up -d weaviate`
   - `uv sync && npm ci --prefix apps/web`
2) Verify:
   - Backend unit tests: `uv run pytest -q`
   - Web build: `npm run build --prefix apps/web`
3) If tests fail: fix and rerun until green.

## PR expectations
- Title: concise; Body: what changed + why.
- Include a short “Demo steps” in the PR body.
- Do not merge; **human review required**.

## Guardrails
- No secrets in code.
- Keep deletions small and reversible.
- Avoid introducing new long-running background jobs.
