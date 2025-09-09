"""
Weaviate bootstrap package for crisis document vectorization.
"""

from .client import WeaviateClient, init_weaviate
from .loader import DocumentProcessor, DocumentIngester, ingest_crisis_documents
from .schema import get_schema

__all__ = [
    'WeaviateClient',
    'init_weaviate',
    'DocumentProcessor', 
    'DocumentIngester',
    'ingest_crisis_documents',
    'get_schema'
]