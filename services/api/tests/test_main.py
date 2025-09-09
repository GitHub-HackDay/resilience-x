"""Tests for the Resilience-X API fallback functionality."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ask_endpoint_cleanup_question():
    """Test /ask endpoint with cleanup-related question."""
    response = client.post("/ask", json={"question": "Which areas have cleanup delays?"})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "answer" in data
    assert "explanation_bullets" in data
    assert "sources" in data
    assert isinstance(data["explanation_bullets"], list)
    assert isinstance(data["sources"], list)
    assert len(data["explanation_bullets"]) > 0
    assert len(data["sources"]) > 0

def test_ask_endpoint_road_question():
    """Test /ask endpoint with road-related question."""
    response = client.post("/ask", json={"question": "Which roads are blocked near Redmond?"})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "SR-520" in data["answer"]
    assert len(data["explanation_bullets"]) == 3
    assert len(data["sources"]) == 3

def test_ask_endpoint_empty_question():
    """Test /ask endpoint with empty question returns error."""
    response = client.post("/ask", json={"question": ""})
    
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]

def test_ask_endpoint_generic_question():
    """Test /ask endpoint with generic question returns default fallback."""
    response = client.post("/ask", json={"question": "What's the weather?"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return default cleanup delays fallback
    assert "King County" in data["answer"]
    assert "crew shortages" in data["answer"]

def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["fallback_mode"] == True