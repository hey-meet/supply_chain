# Week 3 Day 5: Real-Time Analytics Processing Pipeline
def calculate_throughput_efficiency(processed_orders: int, total_capacity: int) -> float:
    if total_capacity <= 0:
        return 0.0
    return round((processed_orders / total_capacity) * 100, 2)
