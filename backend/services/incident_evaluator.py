# Week 3 Day 7: Incident Evaluator wired with Resilience Rerouting Simulator
from backend.services.resilience_simulator import simulate_network_node_failure

def process_active_incidents(incident_id: str, raw_score: float):
    classification = "CRITICAL_DISRUPTION" if raw_score >= 0.8 else "NOMINAL"
    active_routes = [{"node_id": "Node-Edge-4"}, {"node_id": "Node-Edge-5"}]
    
    # Run resilience simulation if critical disruption detected
    if classification == "CRITICAL_DISRUPTION":
        active_routes = simulate_network_node_failure(active_routes, "Node-Edge-4")

    return {
        "incident_id": incident_id,
        "node_impacted": "Node-Edge-4",
        "severity": classification,
        "available_routes_count": len(active_routes),
        "processed_dynamically": True
    }
