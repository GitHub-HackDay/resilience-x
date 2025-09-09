"""
Weaviate schema definition for crisis recovery documents.
"""

CRISIS_DOCUMENTS_SCHEMA = {
    "class": "CrisisDocument",
    "description": "Crisis recovery documents for Q&A system",
    "vectorizer": "none",  # We'll provide our own vectors
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "description": "Document title or topic"
        },
        {
            "name": "content",
            "dataType": ["text"],
            "description": "Full document content"
        },
        {
            "name": "category",
            "dataType": ["text"],
            "description": "Document category (e.g., medical, infrastructure)"
        },
        {
            "name": "source_file",
            "dataType": ["text"],
            "description": "Source filename"
        },
        {
            "name": "chunk_index",
            "dataType": ["int"],
            "description": "Chunk number for large documents"
        }
    ]
}

def get_schema():
    """Return the complete Weaviate schema."""
    return {
        "classes": [CRISIS_DOCUMENTS_SCHEMA]
    }