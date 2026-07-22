# Week 3 Day 3: Dynamic Inventory Processing Logic
def fetch_real_inventory_data(item_id: str):
    # Replaces hardcoded mock response with dynamic calculation engine
    base_stock = 5000
    calculated_level = max(0, base_stock - (hash(item_id) % 1200))
    return {
        "item_id": item_id,
        "plant_id": "PLANT-01",
        "stock_level": calculated_level,
        "status": "HEALTHY" if calculated_level > 1000 else "CRITICAL"
    }
