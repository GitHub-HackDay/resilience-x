"""
Tests for the /ask endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ask_endpoint_success():
    """Test /ask endpoint with valid question."""
    question = "Which neighborhoods are facing cleanup delays?"
    response = client.post("/ask", json={"question": question})
    
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


def test_ask_endpoint_empty_question():
    """Test /ask endpoint with empty question."""
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422  # Validation error


def test_ask_endpoint_missing_question():
    """Test /ask endpoint with missing question field."""
    response = client.post("/ask", json={})
    assert response.status_code == 422  # Validation error


def test_ask_endpoint_long_question():
    """Test /ask endpoint with very long question."""
    long_question = "x" * 501  # Exceeds max_length of 500
    response = client.post("/ask", json={"question": long_question})
    assert response.status_code == 422  # Validation error


def test_ask_endpoint_different_questions():
    """Test /ask endpoint with different types of questions."""
    questions = [
        "What are the main recovery bottlenecks?",
        "Which roads are blocked?",
        "How can we speed up cleanup operations?"
    ]
    
    for question in questions:
        response = client.post("/ask", json={"question": question})
        assert response.status_code == 200
        
        data = response.json()
        assert data["answer"]
        assert data["explanation_bullets"]
        assert isinstance(data["sources"], list)