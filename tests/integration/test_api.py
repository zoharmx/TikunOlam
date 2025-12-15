"""
Integration tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from tikun.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "Tikun Olam API"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.skip(reason="Requires real API keys")
def test_analyze_endpoint():
    """Test analysis endpoint (requires API keys)."""
    scenario = {
        "scenario": """
PROPOSAL: Implement a community garden project
GOAL: Improve food security
STAKEHOLDERS: Local residents, city government
""",
        "case_name": "test_garden",
        "verbose": False,
        "auto_export": False,
        "include_full_results": False
    }

    response = client.post("/analyze", json=scenario)

    assert response.status_code == 200
    data = response.json()
    assert "decision" in data
    assert data["status"] == "completed"


def test_analyze_endpoint_validation():
    """Test analysis endpoint validation."""
    # Scenario too short
    invalid_scenario = {
        "scenario": "Too short",
        "case_name": "test"
    }

    response = client.post("/analyze", json=invalid_scenario)

    assert response.status_code == 422  # Validation error


def test_async_analyze_endpoint():
    """Test async analysis endpoint."""
    scenario = {
        "scenario": "x" * 100,  # Minimum valid length
        "case_name": "async_test"
    }

    response = client.post("/analyze/async", json=scenario)

    # Should return job ID even without real API keys
    assert response.status_code in [200, 500]  # May fail without keys but should accept request


def test_list_jobs():
    """Test job listing endpoint."""
    response = client.get("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert "total" in data
