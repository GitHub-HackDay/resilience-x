"""
Weaviate client integration for semantic search and document retrieval.
"""
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import weaviate
from weaviate.classes.config import Configure


logger = logging.getLogger(__name__)


@dataclass
class RetrievedDocument:
    """Represents a document retrieved from Weaviate."""
    content: str
    source: str
    score: float
    metadata: Dict[str, Any]


class WeaviateClient:
    """Client for interacting with Weaviate vector database."""
    
    def __init__(self, url: str = "http://localhost:8080", timeout: float = 10.0):
        """Initialize the Weaviate client.
        
        Args:
            url: Weaviate instance URL
            timeout: Request timeout in seconds
        """
        self.url = url
        self.timeout = timeout
        self._client: Optional[weaviate.WeaviateClient] = None
        
    def connect(self) -> bool:
        """Connect to Weaviate and check if it's ready.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._client = weaviate.connect_to_local(
                host=self.url.replace("http://", "").replace("https://", ""),
                port=8080
            )
            # Test connection
            self._client.is_ready()
            logger.info(f"Successfully connected to Weaviate at {self.url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {str(e)}")
            self._client = None
            return False
    
    def close(self):
        """Close the Weaviate connection."""
        if self._client:
            self._client.close()
            self._client = None
    
    def search_documents(self, query: str, limit: int = 5) -> List[RetrievedDocument]:
        """Search for documents using semantic similarity.
        
        Args:
            query: Search query
            limit: Maximum number of documents to return
            
        Returns:
            List of retrieved documents sorted by relevance
        """
        if not self._client:
            logger.warning("Weaviate client not connected")
            return []
            
        try:
            # Use the 'Document' collection (we'll need to create this schema)
            documents = self._client.collections.get("Document")
            
            response = documents.query.near_text(
                query=query,
                limit=limit,
                return_metadata=weaviate.classes.query.MetadataQuery(score=True)
            )
            
            results = []
            for item in response.objects:
                doc = RetrievedDocument(
                    content=item.properties.get("content", ""),
                    source=item.properties.get("source", "Unknown"),
                    score=item.metadata.score if item.metadata and item.metadata.score else 0.0,
                    metadata=item.properties
                )
                results.append(doc)
            
            logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def create_schema_if_not_exists(self):
        """Create the Document collection schema if it doesn't exist."""
        if not self._client:
            logger.warning("Weaviate client not connected")
            return False
            
        try:
            # Check if collection exists
            collections = self._client.collections.list_all()
            if "Document" not in [c.name for c in collections]:
                # Create the Document collection
                self._client.collections.create(
                    name="Document",
                    vectorizer_config=Configure.Vectorizer.text2vec_openai(
                        model="ada",
                        model_version="002"
                    ),
                    properties=[
                        weaviate.classes.config.Property(
                            name="content",
                            data_type=weaviate.classes.config.DataType.TEXT,
                            description="Document content"
                        ),
                        weaviate.classes.config.Property(
                            name="source",
                            data_type=weaviate.classes.config.DataType.TEXT,
                            description="Document source/filename"
                        ),
                        weaviate.classes.config.Property(
                            name="title",
                            data_type=weaviate.classes.config.DataType.TEXT,
                            description="Document title"
                        )
                    ]
                )
                logger.info("Created Document collection schema")
            return True
        except Exception as e:
            logger.error(f"Error creating schema: {str(e)}")
            return False


# Global client instance
weaviate_client = WeaviateClient()