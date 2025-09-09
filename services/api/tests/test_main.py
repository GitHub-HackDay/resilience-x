"""
Tests for the main FastAPI application endpoints.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app
from models import QuestionRequest, AskResponse


class TestAskEndpoint:
    """Test cases for the /ask endpoint."""
    
    def test_ask_endpoint_with_results(self, client: TestClient, mock_weaviate_client, sample_documents):
        """Test /ask endpoint when Weaviate returns results."""
        # Mock the search to return sample documents
        mock_weaviate_client.search_documents.return_value = sample_documents
        
        response = client.post("/ask", json={"question": "Which areas have cleanup delays?"})
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "answer" in data
        assert "explanation_bullets" in data  
        assert "sources" in data
        
        # Check content
        assert len(data["explanation_bullets"]) > 0
        assert len(data["sources"]) > 0
        assert "King County" in data["answer"]
    
    def test_ask_endpoint_no_results(self, client: TestClient, mock_weaviate_client):
        """Test /ask endpoint when no documents are found."""
        # Mock empty search results
        mock_weaviate_client.search_documents.return_value = []
        
        response = client.post("/ask", json={"question": "What about Mars cleanup?"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "couldn't find specific information" in data["answer"]
        assert "No semantically similar content was found" in data["explanation_bullets"]
        assert data["sources"] == ["No sources found"]
    
    def test_ask_endpoint_empty_question(self, client: TestClient):
        """Test /ask endpoint with empty question."""
        response = client.post("/ask", json={"question": ""})
        
        assert response.status_code == 400
        assert "Question cannot be empty" in response.json()["detail"]
    
    def test_ask_endpoint_weaviate_error(self, client: TestClient, mock_weaviate_client):
        """Test /ask endpoint when Weaviate throws an error."""
        # Mock Weaviate to raise an exception
        mock_weaviate_client.search_documents.side_effect = Exception("Connection failed")
        
        response = client.post("/ask", json={"question": "Test question"})
        
        assert response.status_code == 200  # Fallback response, not error
        data = response.json()
        
        assert "currently unable to access" in data["answer"]
        assert "vector database" in data["explanation_bullets"][0]


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_endpoint(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "weaviate_connected" in data


class TestRootEndpoint:
    """Test cases for the root endpoint."""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "Resilience-X API" in data["message"]
        assert "endpoints" in data
        assert "ask" in data["endpoints"]