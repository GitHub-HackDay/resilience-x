"""
Weaviate client for semantic search in crisis recovery documents.

This client provides an interface to Weaviate for document storage, 
vectorization, and semantic search operations.
"""

from typing import Dict, List, Optional, Any
import asyncio
import logging
import os

try:
    import weaviate
    from weaviate.classes.config import Configure
except ImportError:
    weaviate = None
    logger = logging.getLogger(__name__)
    logger.warning("Weaviate client not available - install weaviate-client")

logger = logging.getLogger(__name__)


class WeaviateClient:
    """Client for Weaviate vector database operations."""
    
    def __init__(self):
        """Initialize the Weaviate client."""
        self.client = None
        self.is_initialized = False
        self.collection_name = "CrisisDocuments"
        self.weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    
    async def initialize(self) -> None:
        """Initialize the Weaviate client and create schema if needed."""
        if not weaviate:
            logger.warning("Weaviate client not available, using mock implementation")
            self.is_initialized = True
            return
        
        try:
            logger.info(f"Connecting to Weaviate at {self.weaviate_url}...")
            
            # Connect to Weaviate
            self.client = weaviate.connect_to_local(
                host=self.weaviate_url.replace("http://", "").replace(":8080", ""),
                port=8080
            )
            
            # Check connection
            if not self.client.is_ready():
                logger.warning("Weaviate not ready, using mock implementation")
                self.client = None
                self.is_initialized = True
                return
            
            # Create collection if it doesn't exist
            await self._ensure_collection_exists()
            
            self.is_initialized = True
            logger.info("Weaviate client initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to connect to Weaviate: {e}, using mock implementation")
            self.client = None
            self.is_initialized = True
    
    async def search_documents(
        self, 
        query: str, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for documents semantically similar to the query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries with text, source, and metadata
        """
        if not self.is_initialized:
            raise RuntimeError("Weaviate client not initialized")
        
        try:
            logger.info(f"Searching for documents: {query}")
            
            if not self.client:
                # Return mock results
                return await self._mock_search(query, limit)
            
            # Perform actual Weaviate search
            collection = self.client.collections.get(self.collection_name)
            
            response = collection.query.near_text(
                query=query,
                limit=limit,
                return_metadata=["score", "distance"]
            )
            
            results = []
            for item in response.objects:
                results.append({
                    "text": item.properties.get("text", ""),
                    "source": item.properties.get("source", "Unknown"),
                    "metadata": item.properties.get("metadata", {}),
                    "score": item.metadata.score if hasattr(item.metadata, 'score') else 0.0
                })
            
            logger.info(f"Found {len(results)} relevant documents")
            return results
            
        except Exception as e:
            logger.error(f"Document search failed: {e}")
            # Fallback to mock search
            return await self._mock_search(query, limit)
    
    async def _mock_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Mock search implementation for demonstration purposes."""
        logger.info("Using mock Weaviate search")
        
        # Simulate processing time
        await asyncio.sleep(0.2)
        
        # Mock documents based on query patterns
        mock_docs = []
        
        if "cleanup" in query.lower() or "delay" in query.lower():
            mock_docs = [
                {
                    "text": "Cleanup operations in King County are experiencing significant delays due to crew shortages. Three major contractors have reported staffing at 60% capacity, impacting debris removal timelines.",
                    "source": "King County Emergency Response Report - Section 3.2",
                    "metadata": {"date": "2024-01-15", "priority": "high"},
                    "score": 0.92
                },
                {
                    "text": "Debris processing facilities are operating at 150% capacity, causing bottlenecks in the cleanup pipeline. Additional temporary sites are being established.",
                    "source": "Debris Processing Facility Status Report",
                    "metadata": {"date": "2024-01-14", "facility": "King County Central"},
                    "score": 0.87
                }
            ]
        
        elif "road" in query.lower() or "block" in query.lower():
            mock_docs = [
                {
                    "text": "State Route 520 eastbound remains closed between Redmond and Bellevue due to fallen trees across multiple lanes. Heavy equipment access is limited by additional debris.",
                    "source": "Washington State DOT Traffic Report",
                    "metadata": {"date": "2024-01-15", "route": "SR-520"},
                    "score": 0.94
                },
                {
                    "text": "I-405 northbound has partial closures near Exit 14 (SR-520). Two lanes remain open but significant delays expected through evening hours.",
                    "source": "Emergency Services Routing Update", 
                    "metadata": {"date": "2024-01-15", "route": "I-405"},
                    "score": 0.89
                }
            ]
        
        elif "neighborhood" in query.lower():
            mock_docs = [
                {
                    "text": "Bellevue downtown district showing highest concentration of unresolved service requests. Power restoration ongoing with estimated completion by midnight.",
                    "source": "Emergency Services Database - Query Results",
                    "metadata": {"date": "2024-01-15", "area": "Bellevue downtown"},
                    "score": 0.91
                },
                {
                    "text": "Redmond residential areas experiencing communication infrastructure issues. Temporary cell towers deployed to three locations.",
                    "source": "Communication Infrastructure Status",
                    "metadata": {"date": "2024-01-15", "area": "Redmond residential"},
                    "score": 0.85
                }
            ]
        
        else:
            # Generic crisis-related documents
            mock_docs = [
                {
                    "text": "Emergency response teams have established command centers at three locations. Coordination with local agencies proceeding according to established protocols.",
                    "source": "Crisis Response Coordination Log",
                    "metadata": {"date": "2024-01-15", "type": "coordination"},
                    "score": 0.75
                },
                {
                    "text": "Resource allocation status: Medical supplies at 80% capacity, emergency shelters at 65% capacity. Additional resources being mobilized.",
                    "source": "Resource Allocation Status Report",
                    "metadata": {"date": "2024-01-15", "type": "resources"},
                    "score": 0.70
                }
            ]
        
        return mock_docs[:limit]
    
    async def _ensure_collection_exists(self) -> None:
        """Create the documents collection if it doesn't exist."""
        if not self.client:
            return
        
        try:
            # Check if collection exists
            if self.client.collections.exists(self.collection_name):
                logger.info(f"Collection {self.collection_name} already exists")
                return
            
            # Create collection with schema
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=Configure.Vectorizer.text2vec_openai(),
                properties=[
                    weaviate.classes.config.Property(
                        name="text",
                        data_type=weaviate.classes.config.DataType.TEXT,
                        description="The main text content of the document"
                    ),
                    weaviate.classes.config.Property(
                        name="source", 
                        data_type=weaviate.classes.config.DataType.TEXT,
                        description="The source of the document"
                    ),
                    weaviate.classes.config.Property(
                        name="metadata",
                        data_type=weaviate.classes.config.DataType.OBJECT,
                        description="Additional metadata about the document"
                    )
                ]
            )
            
            logger.info(f"Created collection {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise
    
    async def close(self) -> None:
        """Clean up resources."""
        logger.info("Closing Weaviate client...")
        if self.client:
            self.client.close()
        self.is_initialized = False