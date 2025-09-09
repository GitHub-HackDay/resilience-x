"""
Tests for the Resilience-X FastAPI backend.
"""

import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resilience-X API is running"}


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "resilience-x-api"
    assert "version" in data


def test_ask_endpoint_success():
    """Test the /ask endpoint with a valid question."""
    question_data = {"question": "Which neighborhoods are facing cleanup delays?"}
    response = client.post("/ask", json=question_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "answer" in data
    assert "explanation_bullets" in data
    assert "sources" in data
    
    # Check data types
    assert isinstance(data["answer"], str)
    assert isinstance(data["explanation_bullets"], list)
    assert isinstance(data["sources"], list)
    
    # Check content is not empty
    assert len(data["answer"]) > 0
    assert len(data["explanation_bullets"]) > 0
    assert len(data["sources"]) > 0


def test_ask_endpoint_empty_question():
    """Test the /ask endpoint with an empty question."""
    question_data = {"question": ""}
    response = client.post("/ask", json=question_data)
    
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]


def test_ask_endpoint_whitespace_question():
    """Test the /ask endpoint with whitespace-only question."""
    question_data = {"question": "   "}
    response = client.post("/ask", json=question_data)
    
    assert response.status_code == 400


def test_ask_endpoint_different_question_types():
    """Test the /ask endpoint with different question types to verify mock responses."""
    
    # Test cleanup-related question
    cleanup_question = {"question": "Why are cleanup efforts delayed?"}
    response = client.post("/ask", json=cleanup_question)
    assert response.status_code == 200
    data = response.json()
    assert "cleanup" in data["answer"].lower() or "delay" in data["answer"].lower()
    
    # Test road-related question  
    road_question = {"question": "Which roads are blocked?"}
    response = client.post("/ask", json=road_question)
    assert response.status_code == 200
    data = response.json()
    assert "road" in data["answer"].lower() or "blocked" in data["answer"].lower()
    
    # Test general question
    general_question = {"question": "What is the current status?"}
    response = client.post("/ask", json=general_question)
    assert response.status_code == 200
    data = response.json()
    assert len(data["answer"]) > 0


def test_ask_endpoint_invalid_json():
    """Test the /ask endpoint with invalid JSON structure."""
    response = client.post("/ask", json={"wrong_field": "test"})
    assert response.status_code == 422  # Validation error