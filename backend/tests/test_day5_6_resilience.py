from backend.services.analytics_pipeline import calculate_throughput_efficiency
from backend.services.resilience_simulator import simulate_network_node_failure

def test_throughput_efficiency():
    assert calculate_throughput_efficiency(80, 100) == 80.0

def test_node_fault_simulation():
    routes = [{"node_id": "N1"}, {"node_id": "N2"}]
    assert len(simulate_network_node_failure(routes, "N1")) == 1
