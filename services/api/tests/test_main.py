"""
Basic tests for the Resilience-X API.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "resilience-x-api"


def test_ask_endpoint():
    """Test the /ask endpoint with a sample question."""
    response = client.post(
        "/ask",
        json={"question": "Which neighborhoods are facing cleanup delays?"}
    )
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


def test_ask_empty_question():
    """Test /ask endpoint with empty question."""
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 200  # Should still work with fallback


def test_ask_invalid_request():
    """Test /ask endpoint with invalid request body."""
    response = client.post("/ask", json={})
    assert response.status_code == 422  # Validation error