# backend/tests/test_api_v1.py
from backend.config import settings

def test_settings_initialization():
    """Verify that the system configuration loads baseline values cleanly."""
    assert settings.APP_NAME == "Logistics Autonomous Disruption Monitoring Agent"
    assert settings.API_V1_STR == "/api/v1"
    assert isinstance(settings.DEBUG, bool)