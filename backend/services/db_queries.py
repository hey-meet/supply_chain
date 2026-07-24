# Week 3 Day 4: Optimized Query Processing
import asyncio

async def fetch_plant_metrics_async(plant_id: str):
    # Simulates optimized async database fetch minimizing I/O latency
    await asyncio.sleep(0.01)
    return {
        "plant_id": plant_id,
        "operational_status": "active",
        "capacity_utilization": 0.89
    }
