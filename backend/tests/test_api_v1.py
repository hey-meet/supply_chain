# backend/tests/test_api_v1.py
from backend.config import settings


# Append to backend/tests/test_api_v1.py
from backend.api.schemas import SystemStatusResponse


# Append to backend/tests/test_api_v1.py
from fastapi.testclient import TestClient
from backend.main import app




# Append to backend/tests/test_api_v1.py
def test_telemetry_sanitization_and_bounds():
    """Ensure data layers strip illegal characters and reject corrupt GPS bounds."""
    # Test valid input with messy spacing and invalid symbols
    payload = {
        "tracking_id": "  CONT-12345!@#  ",
        "origin_country": "IND",
        "latitude": 18.5204,
        "longitude": 73.8567
    }
    response = client.post("/api/v1/telemetry/validate", json=payload)
    assert response.status_code == 201
    assert response.json()["sanitized_tracking_id"] == "CONT-12345"

    # Test out-of-bounds latitude
    bad_payload = payload.copy()
    bad_payload["latitude"] = 120.0  # Invalid latitude
    bad_response = client.post("/api/v1/telemetry/validate", json=bad_payload)
    assert bad_response.status_code == 422  # Unprocessable Entity



# Append this inside the existing test_telemetry_sanitization_and_bounds() function or add it right below:

def test_telemetry_invalid_longitude_bounds():
    """Ensure that geographic longitude constraints throw a 422 error for out-of-bounds parameters."""
    from backend.tests.test_api_v1 import client
    
    bad_longitude_payload = {
        "tracking_id": "CONT-99999",
        "origin_country": "IND",
        "latitude": 18.5204,
        "longitude": 200.0  # Invalid longitude (> 180.0)
    }
    response = client.post("/api/v1/telemetry/validate", json=bad_longitude_payload)
    assert response.status_code == 422





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





# Append to backend/tests/test_api_v1.py

def test_async_ingestion_returns_202():
    """Verify that the async route returns 202 Accepted status immediately."""
    from backend.tests.test_api_v1 import client
    
    test_payload = {"raw_text": "Breaking: Supply chain route disruptions reported at main port terminals."}
    response = client.post("/api/v1/news/ingest-async", params=test_payload)
    
    assert response.status_code == 202
    assert response.json()["success"] is True
    assert "payload_id" in response.json()
