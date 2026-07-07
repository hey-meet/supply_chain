# backend/tests/test_api_v1.py
from backend.config import settings


# Append to backend/tests/test_api_v1.py
from backend.api.schemas import SystemStatusResponse


# Append to backend/tests/test_api_v1.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_live_app_status_endpoint():
    """Execute end-to-end client integration check against server health routes."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_system_status_schema_validation():
    """Ensure response schemas correctly validate structure and strictly enforce types."""
    payload = {"app_name": "Test Runner", "environment": "test", "active_monitors": []}
    validated = SystemStatusResponse(**payload)
    assert validated.status == "healthy"
    assert validated.app_name == "Test Runner"

def test_settings_initialization():
    """Verify that the system configuration loads baseline values cleanly."""
    assert settings.APP_NAME == "Logistics Autonomous Disruption Monitoring Agent"
    assert settings.API_V1_STR == "/api/v1"
    assert isinstance(settings.DEBUG, bool)