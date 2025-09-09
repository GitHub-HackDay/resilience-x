"""
Tests for the Weaviate client integration.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from clients.weaviate_client import WeaviateClient, RetrievedDocument


class TestWeaviateClient:
    """Test cases for WeaviateClient."""
    
    def test_client_initialization(self):
        """Test client initialization with default parameters."""
        client = WeaviateClient()
        
        assert client.url == "http://localhost:8080"
        assert client.timeout == 10.0
        assert client._client is None
    
    def test_client_initialization_custom(self):
        """Test client initialization with custom parameters.""" 
        client = WeaviateClient(url="http://custom:8080", timeout=30.0)
        
        assert client.url == "http://custom:8080"
        assert client.timeout == 30.0
    
    @patch('clients.weaviate_client.weaviate')
    def test_connect_success(self, mock_weaviate):
        """Test successful connection to Weaviate."""
        mock_client = Mock()
        mock_client.is_ready.return_value = True
        mock_weaviate.connect_to_local.return_value = mock_client
        
        client = WeaviateClient()
        result = client.connect()
        
        assert result is True
        assert client._client == mock_client
        mock_weaviate.connect_to_local.assert_called_once()
    
    @patch('clients.weaviate_client.weaviate')
    def test_connect_failure(self, mock_weaviate):
        """Test connection failure to Weaviate."""
        mock_weaviate.connect_to_local.side_effect = Exception("Connection failed")
        
        client = WeaviateClient()
        result = client.connect()
        
        assert result is False
        assert client._client is None
    
    def test_search_documents_no_client(self):
        """Test search when client is not connected."""
        client = WeaviateClient()
        
        results = client.search_documents("test query")
        
        assert results == []
    
    @patch('clients.weaviate_client.weaviate')  
    def test_search_documents_success(self, mock_weaviate):
        """Test successful document search."""
        # Setup mock client and response
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.collections.get.return_value = mock_collection
        
        # Mock search response
        mock_item = Mock()
        mock_item.properties = {
            "content": "Test document content",
            "source": "test.pdf",
            "title": "Test Document"
        }
        mock_item.metadata = Mock()
        mock_item.metadata.score = 0.85
        
        mock_response = Mock()
        mock_response.objects = [mock_item]
        mock_collection.query.near_text.return_value = mock_response
        
        client = WeaviateClient()
        client._client = mock_client
        
        results = client.search_documents("test query", limit=3)
        
        assert len(results) == 1
        assert isinstance(results[0], RetrievedDocument)
        assert results[0].content == "Test document content"
        assert results[0].source == "test.pdf"
        assert results[0].score == 0.85
        
        mock_collection.query.near_text.assert_called_once_with(
            query="test query",
            limit=3,
            return_metadata=mock_weaviate.classes.query.MetadataQuery(score=True)
        )
    
    def test_search_documents_exception(self):
        """Test search when an exception occurs."""
        mock_client = Mock()
        mock_client.collections.get.side_effect = Exception("Search failed")
        
        client = WeaviateClient()
        client._client = mock_client
        
        results = client.search_documents("test query")
        
        assert results == []
    
    def test_close_client(self):
        """Test closing the client connection."""
        mock_client = Mock()
        
        client = WeaviateClient()
        client._client = mock_client
        
        client.close()
        
        mock_client.close.assert_called_once()
        assert client._client is None