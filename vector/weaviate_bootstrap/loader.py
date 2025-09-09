"""
Document loader and vectorization utilities.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from .client import WeaviateClient

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes documents and creates embeddings for Weaviate ingestion."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize document processor.
        
        Args:
            model_name: Sentence transformer model name for embeddings
        """
        self.model_name = model_name
        self.model = None
    
    def _load_model(self):
        """Load sentence transformer model."""
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
    
    def load_documents(self, data_dir: str) -> List[Dict[str, Any]]:
        """Load documents from directory.
        
        Args:
            data_dir: Directory containing text files
            
        Returns:
            List of document dictionaries
        """
        documents = []
        data_path = Path(data_dir)
        
        if not data_path.exists():
            logger.error(f"Data directory not found: {data_dir}")
            return documents
        
        for file_path in data_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                # Extract title from first line
                lines = content.split('\n')
                title = lines[0].strip() if lines else file_path.stem
                
                # Categorize based on filename
                category = self._categorize_document(file_path.stem)
                
                documents.append({
                    'title': title,
                    'content': content,
                    'category': category,
                    'source_file': file_path.name,
                    'chunk_index': 0
                })
                
                logger.info(f"Loaded document: {file_path.name}")
                
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
        
        return documents
    
    def _categorize_document(self, filename: str) -> str:
        """Categorize document based on filename.
        
        Args:
            filename: Document filename (without extension)
            
        Returns:
            Category string
        """
        category_map = {
            'building_assessment': 'Infrastructure',
            'water_distribution': 'Utilities',
            'communications': 'Communications',
            'power_recovery': 'Utilities',
            'medical_response': 'Medical',
            'transportation_recovery': 'Infrastructure',
            'shelter_management': 'Housing',
            'debris_management': 'Recovery',
            'economic_recovery': 'Economy'
        }
        
        return category_map.get(filename, 'General')
    
    def create_embeddings(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create embeddings for documents.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Documents with embeddings added
        """
        self._load_model()
        
        # Extract content for embedding
        texts = [doc['content'] for doc in documents]
        
        logger.info(f"Creating embeddings for {len(texts)} documents")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Add embeddings to documents
        for doc, embedding in zip(documents, embeddings):
            doc['embedding'] = embedding.tolist()
        
        return documents


class DocumentIngester:
    """Ingests processed documents into Weaviate."""
    
    def __init__(self, weaviate_client: WeaviateClient):
        """Initialize document ingester.
        
        Args:
            weaviate_client: Connected WeaviateClient instance
        """
        self.client = weaviate_client
    
    def ingest_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Ingest documents into Weaviate.
        
        Args:
            documents: List of processed documents with embeddings
            
        Returns:
            True if ingestion successful, False otherwise
        """
        try:
            collection = self.client.client.collections.get("CrisisDocument")
            
            # Clear existing documents
            collection.data.delete_many(where={})
            
            # Batch insert documents
            with collection.batch.dynamic() as batch:
                for doc in documents:
                    # Extract embedding
                    vector = doc.pop('embedding', None)
                    
                    # Add document
                    batch.add_object(
                        properties=doc,
                        vector=vector
                    )
            
            logger.info(f"Ingested {len(documents)} documents into Weaviate")
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            return False


def ingest_crisis_documents(
    data_dir: str,
    weaviate_url: str = "http://localhost:8080",
    weaviate_api_key: Optional[str] = None
) -> bool:
    """Complete document ingestion pipeline.
    
    Args:
        data_dir: Directory containing crisis documents
        weaviate_url: Weaviate instance URL
        weaviate_api_key: API key for authentication
        
    Returns:
        True if ingestion successful, False otherwise
    """
    # Initialize Weaviate client
    from .client import init_weaviate
    
    weaviate_client = init_weaviate(weaviate_url, weaviate_api_key)
    if not weaviate_client:
        return False
    
    try:
        # Process documents
        processor = DocumentProcessor()
        documents = processor.load_documents(data_dir)
        
        if not documents:
            logger.error("No documents found to ingest")
            return False
        
        # Create embeddings
        documents = processor.create_embeddings(documents)
        
        # Ingest into Weaviate
        ingester = DocumentIngester(weaviate_client)
        success = ingester.ingest_documents(documents)
        
        return success
        
    finally:
        weaviate_client.close()