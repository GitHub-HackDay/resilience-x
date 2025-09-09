"""
Unit tests for the main FastAPI application
Tests basic endpoint functionality and request/response models
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the services/api directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../services/api"))

from main import app, AskRequest, AskResponse


class TestHealthEndpoint:
    """Test cases for the health check endpoint"""
    
    def test_health_check_success(self):
        """Test health check returns correct status"""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "resilience-x-api"


class TestAskEndpoint:
    """Test cases for the main /ask endpoint"""
    
    def test_ask_endpoint_happy_path(self):
        """Test successful question processing"""
        client = TestClient(app)
        
        request_data = {
            "question": "Which neighborhoods are facing cleanup delays?"
        }
        
        response = client.post("/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "answer" in data
        assert "explanation_bullets" in data
        assert "sources" in data
        assert isinstance(data["explanation_bullets"], list)
        assert isinstance(data["sources"], list)
        
        # Verify content is not empty
        assert len(data["answer"]) > 0
        assert len(data["explanation_bullets"]) > 0
        assert len(data["sources"]) > 0
    
    def test_ask_endpoint_empty_question(self):
        """Test handling of empty question - negative test case"""
        client = TestClient(app)
        
        request_data = {
            "question": ""
        }
        
        response = client.post("/ask", json=request_data)
        
        # Should still return 200 but with appropriate response
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
    
    def test_ask_endpoint_missing_question_field(self):
        """Test handling of malformed request - negative test case"""
        client = TestClient(app)
        
        request_data = {}  # Missing question field
        
        response = client.post("/ask", json=request_data)
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_ask_endpoint_invalid_json(self):
        """Test handling of invalid JSON - negative test case"""
        client = TestClient(app)
        
        response = client.post("/ask", data="invalid json")
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_ask_endpoint_very_long_question(self):
        """Test handling of extremely long questions"""
        client = TestClient(app)
        
        # Create a very long question (1000 characters)
        long_question = "What is the status of " + "recovery " * 140 + "efforts?"
        
        request_data = {
            "question": long_question
        }
        
        response = client.post("/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data


class TestPydanticModels:
    """Test cases for request/response models"""
    
    def test_ask_request_model_valid(self):
        """Test AskRequest model with valid data"""
        request = AskRequest(question="Test question?")
        assert request.question == "Test question?"
    
    def test_ask_request_model_empty_string(self):
        """Test AskRequest model with empty string"""
        request = AskRequest(question="")
        assert request.question == ""
    
    def test_ask_response_model_valid(self):
        """Test AskResponse model with valid data"""
        response = AskResponse(
            answer="Test answer",
            explanation_bullets=["Point 1", "Point 2"],
            sources=["Source A", "Source B"]
        )
        
        assert response.answer == "Test answer"
        assert len(response.explanation_bullets) == 2
        assert len(response.sources) == 2
    
    def test_ask_response_model_empty_lists(self):
        """Test AskResponse model with empty lists"""
        response = AskResponse(
            answer="Test answer",
            explanation_bullets=[],
            sources=[]
        )
        
        assert response.answer == "Test answer"
        assert len(response.explanation_bullets) == 0
        assert len(response.sources) == 0


class TestCORSConfiguration:
    """Test CORS middleware configuration"""
    
    def test_cors_preflight_request(self):
        """Test CORS preflight request handling"""
        client = TestClient(app)
        
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        }
        
        response = client.options("/ask", headers=headers)
        
        # Should handle preflight request
        assert response.status_code in [200, 204]