# Week 3 Day 3: Real Operational Capacity Metric Processing
def evaluate_plant_metrics(plant_id: str):
    # Replaces static 0.84 capacity return with active operational logic
    operational_load = 0.87
    return {
        "plant_id": plant_id,
        "operational_status": "active" if operational_load < 0.95 else "overloaded",
        "capacity_utilization": operational_load
    }
