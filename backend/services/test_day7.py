from backend.services.day7_monitoring import get_system_health

def test_health_profile():
    assert get_system_health()['status'] == 'healthy'
