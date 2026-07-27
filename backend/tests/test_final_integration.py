from backend.services.final_analytics import compute_network_wide_efficiency
from backend.core.final_contract_guard import enforce_contract_integrity

def test_network_efficiency_calculation():
    plants = [{"capacity_utilization": 0.9}, {"capacity_utilization": 0.8}]
    incidents = [{"severity": "CRITICAL_DISRUPTION"}]
    res = compute_network_wide_efficiency(plants, incidents)
    assert res["network_efficiency_pct"] == 85.0
    assert res["resilience_index"] == 87.5
    assert res["system_status"] == "OPTIMAL"

def test_contract_integrity_guard():
    raw_payload = {"plant_id": "PLANT-01"}
    guarded = enforce_contract_integrity(raw_payload, ["plant_id", "status"])
    assert guarded["status"] == "N/A"
