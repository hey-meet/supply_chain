from backend.services.network_service import calculate_node_risk
from backend.services.reports_service import generate_executive_impact_summary
from backend.core.sanitizer import sanitize_service_payload

def test_node_risk_calculation():
    res = calculate_node_risk(80, 100, 15.0)
    assert res["status"] == "CRITICAL"
    assert res["utilization_rate"] == 80.0

def test_executive_reports_summary():
    disruptions = [{"estimated_loss": 300000, "plant_id": "P1"}, {"estimated_loss": 300000, "plant_id": "P2"}]
    res = generate_executive_impact_summary(disruptions)
    assert res["total_financial_impact"] == 600000
    assert res["impact_severity"] == "HIGH"

def test_payload_sanitizer():
    cleaned = sanitize_service_payload({"node": " Plant-01 "})
    assert cleaned["node"] == "Plant-01"
