# Week 3 Day 7: Plant Service wired with Multi-Node Telemetry
from backend.services.metrics_aggregator import aggregate_supply_chain_telemetry

def evaluate_plant_metrics(plant_id: str):
    raw_nodes = [{"node_id": plant_id, "status": "ACTIVE"}]
    telemetry = aggregate_supply_chain_telemetry(raw_nodes)
    
    return {
        "plant_id": plant_id,
        "operational_status": "active" if telemetry.get("health_score", 0) > 50 else "inactive",
        "capacity_utilization": 0.87,
        "system_health_score": telemetry.get("health_score")
    }
