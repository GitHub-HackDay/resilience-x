"""
Tests for the /ask endpoint.

Tests the main GraphRAG reasoning integration.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from services.api.main import app


class TestAskEndpoint:
    """Test cases for the /ask endpoint."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    def test_ask_endpoint_success(self):
        """Test successful /ask request with mocked clients."""
        # Test data
        request_data = {"question": "Which areas have cleanup delays?"}
        
        # Mock the clients to be available
        with patch('services.api.main.graphrag_client') as mock_graphrag, \
             patch('services.api.main.weaviate_client') as mock_weaviate:
            
            # Configure mocks
            mock_weaviate.search_documents = AsyncMock(return_value=[
                {
                    "text": "King County experiencing cleanup delays",
                    "source": "Emergency Report",
                    "metadata": {},
                    "score": 0.9
                }
            ])
            
            mock_graphrag.query = AsyncMock(return_value={
                "answer": "King County has cleanup delays due to crew shortages",
                "explanation_bullets": [
                    "Semantic search found relevant documents",
                    "GraphRAG analysis identified crew shortage as root cause"
                ],
                "sources": ["Emergency Report"]
            })
            
            # Make request
            response = self.client.post("/ask", json=request_data)
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "explanation_bullets" in data
            assert "sources" in data
            assert isinstance(data["explanation_bullets"], list)
            assert isinstance(data["sources"], list)
    
    def test_ask_endpoint_fallback_when_clients_unavailable(self):
        """Test /ask endpoint returns fallback when clients are None."""
        request_data = {"question": "Test question"}
        
        # Mock clients as None (not initialized)
        with patch('services.api.main.graphrag_client', None), \
             patch('services.api.main.weaviate_client', None):
            
            response = self.client.post("/ask", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "Service temporarily unavailable" in data["answer"]
            assert len(data["explanation_bullets"]) > 0
            assert len(data["sources"]) > 0
    
    def test_ask_endpoint_invalid_request(self):
        """Test /ask endpoint with invalid request data."""
        # Missing required field
        response = self.client.post("/ask", json={})
        assert response.status_code == 422
        
        # Invalid field type
        response = self.client.post("/ask", json={"question": 123})
        assert response.status_code == 422
    
    def test_root_endpoint(self):
        """Test the root health check endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Resilience-X API is running"}