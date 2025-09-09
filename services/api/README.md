# Resilience-X API

FastAPI backend for the Resilience-X crisis recovery Q&A system.

## Features

- `/ask` endpoint for natural language questions
- Integration with Weaviate for semantic search
- GraphRAG for multi-hop reasoning
- Explainable answers with sources

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn main:app --reload --port 8000
```

## Testing

```bash
pytest
```