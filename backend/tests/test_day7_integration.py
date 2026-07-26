from backend.services.inventory_service import fetch_real_inventory_data
from backend.services.plant_service import evaluate_plant_metrics
from backend.services.incident_evaluator import process_active_incidents

def test_inventory_integration():
    res = fetch_real_inventory_data("ITEM-101")
    assert "efficiency_index" in res
    assert res["status"] in ["HEALTHY", "CRITICAL"]

def test_plant_integration():
    res = evaluate_plant_metrics("PLANT-01")
    assert res["operational_status"] == "active"

def test_incident_integration():
    res = process_active_incidents("INC-001", 0.9)
    assert res["severity"] == "CRITICAL_DISRUPTION"
    assert res["available_routes_count"] == 1
