# Week 3 Day 5: Multi-Node Metrics Aggregation
def aggregate_supply_chain_telemetry(node_data: list) -> dict:
    total_nodes = len(node_data)
    active_nodes = sum(1 for node in node_data if node.get("status") == "ACTIVE")
    return {
        "total_nodes": total_nodes,
        "health_score": round((active_nodes / total_nodes) * 100, 2) if total_nodes > 0 else 0.0
    }
