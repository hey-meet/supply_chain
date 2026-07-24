# Week 3 Day 6: Fault Injection & Network Resilience Simulator
def simulate_network_node_failure(active_routes: list, failed_node_id: str) -> list:
    return [route for route in active_routes if route.get("node_id") != failed_node_id]
