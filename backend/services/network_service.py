# Week 4 Day 1: Real Business Logic for Network Capacity & Latency Analysis
def calculate_node_risk(active_shipments: int, node_capacity: int, baseline_delay: float) -> dict:
    utilization = (active_shipments / node_capacity) if node_capacity > 0 else 1.0
    risk_score = round(min(1.0, utilization * 0.7 + (baseline_delay / 100) * 0.3), 2)
    
    return {
        "utilization_rate": round(utilization * 100, 2),
        "risk_score": risk_score,
        "status": "CRITICAL" if risk_score > 0.75 else "STABLE"
    }
