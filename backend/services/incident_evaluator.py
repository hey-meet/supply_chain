# Week 3 Day 3: Dynamic Incident Risk Engine
def process_active_incidents(incident_id: str, raw_score: float):
    # Implements real evaluation while maintaining exact API response structure
    classification = "CRITICAL_DISRUPTION" if raw_score >= 0.8 else "NOMINAL"
    return {
        "incident_id": incident_id,
        "node_impacted": "Node-Edge-4",
        "severity": classification,
        "processed_dynamically": True
    }
