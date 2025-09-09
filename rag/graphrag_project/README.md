# GraphRAG Project Documentation

This directory contains the GraphRAG configuration and pipeline for building a knowledge graph from crisis recovery documents. The knowledge graph enables multi-hop reasoning for the Resilience-X Q&A system.

## Directory Structure

```
rag/graphrag_project/
├── settings.yaml              # GraphRAG configuration
├── build_graph.py            # Graph building pipeline
├── requirements.txt          # Python dependencies
├── prompts/                  # Custom prompts for entity extraction
│   ├── entity_extraction.txt
│   └── summarize_descriptions.txt
├── output/                   # Generated graph files (created after build)
├── cache/                    # Temporary processing files
└── reports/                  # Build reports and logs
```

## Quick Start

1. **Set up environment:**
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Run the setup script:**
   ```bash
   bash scripts/setup_graphrag.sh
   ```

3. **Or build manually:**
   ```bash
   cd rag/graphrag_project
   pip install -r requirements.txt
   python build_graph.py
   ```

## Configuration

The `settings.yaml` file is optimized for crisis recovery documents with:

- **Small dataset processing**: Configured for 5-20 short documents
- **Crisis-specific entities**: Locations, organizations, resources, incidents, timeframes  
- **Efficient processing**: Single-threaded with memory storage for fast iteration
- **OpenAI integration**: Uses GPT-3.5-turbo for extraction and text-embedding-ada-002 for vectors

## Entity Types

The system extracts and relates these entity types:

- **LOCATION**: Geographic areas, neighborhoods, roads, facilities, shelters
- **ORGANIZATION**: Government agencies, utility companies, medical facilities
- **RESOURCE**: Equipment, supplies, personnel, infrastructure, capacity  
- **INCIDENT**: Crisis events, outages, damage, disruptions
- **TIMEFRAME**: Dates, durations, timelines, recovery deadlines

## Output Files

After building the graph, these files are created in the `output/` directory:

- `entities.parquet`: Extracted entities with descriptions and importance scores
- `relationships.parquet`: Entity relationships with strength scores
- `communities.parquet`: Community summaries for global reasoning

## Integration with /ask Endpoint

The knowledge graph is designed to support the FastAPI `/ask` endpoint by:

1. **Local Search**: Finding specific entities and relationships relevant to a question
2. **Global Search**: Using community summaries for broader context  
3. **Multi-hop Reasoning**: Following relationship chains to answer complex questions
4. **Explainability**: Providing source tracing and reasoning steps

## Troubleshooting

**Missing API Key:**
```bash
export OPENAI_API_KEY=your_key_here
```

**No documents found:**
- Ensure `.txt` files exist in `rag/data/`
- Check file permissions and content

**Build failures:**
- Check OpenAI API key validity and quota
- Review logs in `reports/` directory
- Verify document formatting and content

## Sample Questions

The knowledge graph is designed to answer questions like:

- "Which roads are blocked in Redmond and why?"
- "Where are cleanup delays happening and what's causing them?"
- "Which shelters have capacity and where are they located?"
- "What utility outages are affecting medical services?"
- "How long will it take to restore power in Woodinville?"

## Next Steps

After building the graph:

1. Integrate with the FastAPI backend at `services/api/`
2. Connect to Weaviate for hybrid search capabilities
3. Test end-to-end question answering through the `/ask` endpoint
4. Validate explainability and source tracing functionality