"""
Weaviate client and bootstrap utilities for crisis documents.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import weaviate
from weaviate.classes.init import Auth
import weaviate.classes as wvc
from .schema import get_schema

logger = logging.getLogger(__name__)


class WeaviateClient:
    """Client for connecting to and managing Weaviate instance."""
    
    def __init__(self, url: str = "http://localhost:8080", api_key: Optional[str] = None):
        """Initialize Weaviate client.
        
        Args:
            url: Weaviate instance URL
            api_key: API key for authentication (optional for local instance)
        """
        self.url = url
        self.api_key = api_key
        self.client = None
    
    def connect(self) -> bool:
        """Connect to Weaviate instance.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if self.api_key:
                auth_config = Auth.api_key(self.api_key)
                self.client = weaviate.connect_to_custom(
                    http_host=self.url.replace("http://", "").replace("https://", ""),
                    http_port=8080,
                    http_secure=False,
                    auth_credentials=auth_config
                )
            else:
                self.client = weaviate.connect_to_local(
                    host=self.url.replace("http://", "").replace("https://", "").split(":")[0],
                    port=8080
                )
            
            # Test connection
            self.client.collections.list_all()
            logger.info(f"Connected to Weaviate at {self.url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {e}")
            return False
    
    def create_schema(self) -> bool:
        """Create schema in Weaviate.
        
        Returns:
            True if schema created successfully, False otherwise
        """
        try:
            # Check if collection already exists
            collections = self.client.collections.list_all()
            if "CrisisDocument" in [c.name for c in collections]:
                logger.info("CrisisDocument collection already exists")
                return True
            
            # Create collection
            self.client.collections.create(
                name="CrisisDocument",
                description="Crisis recovery documents for Q&A system",
                vectorizer_config=wvc.config.Configure.Vectorizer.none(),
                properties=[
                    wvc.config.Property(
                        name="title",
                        data_type=wvc.config.DataType.TEXT,
                        description="Document title or topic"
                    ),
                    wvc.config.Property(
                        name="content", 
                        data_type=wvc.config.DataType.TEXT,
                        description="Full document content"
                    ),
                    wvc.config.Property(
                        name="category",
                        data_type=wvc.config.DataType.TEXT,
                        description="Document category"
                    ),
                    wvc.config.Property(
                        name="source_file",
                        data_type=wvc.config.DataType.TEXT,
                        description="Source filename"
                    ),
                    wvc.config.Property(
                        name="chunk_index",
                        data_type=wvc.config.DataType.INT,
                        description="Chunk number for large documents"
                    )
                ]
            )
            
            logger.info("Created CrisisDocument collection")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create schema: {e}")
            return False
    
    def close(self):
        """Close Weaviate connection."""
        if self.client:
            self.client.close()
            logger.info("Closed Weaviate connection")


def init_weaviate(url: str = "http://localhost:8080", api_key: Optional[str] = None) -> Optional[WeaviateClient]:
    """Initialize Weaviate client and create schema.
    
    Args:
        url: Weaviate instance URL
        api_key: API key for authentication
        
    Returns:
        WeaviateClient instance if successful, None otherwise
    """
    client = WeaviateClient(url, api_key)
    
    if not client.connect():
        return None
        
    if not client.create_schema():
        client.close()
        return None
        
    return client