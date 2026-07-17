import os
import sys
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.manager import kb_manager
from services.route_optimizer import RouteOptimizerService

class OrderProcessorService:
    def __init__(self):
        self.kb = kb_manager
        self.optimizer = RouteOptimizerService()

    def process_maintenance_order(self, plant_id: str, part_id: str, quantity: int, route_id: str) -> Dict[str, Any]:
        """Simulates processing a replacement part order for a critical maintenance task."""
        plant = self.kb.get_plant_by_id(plant_id)
        if not plant:
            return {"status": "rejected", "reason": f"Plant {plant_id} not recognized."}

        route_check = self.optimizer.validate_route(route_id)
        if not route_check.get("is_operable", False):
            return {
                "status": "held",
                "reason": "Target logistics route is inactive or blocked.",
                "route_details": route_check
            }

        estimated_hours = self.optimizer.calculate_estimated_delay(route_id, weather_factor=1.2)
        
        return {
            "status": "approved",
            "plant_name": plant.get("name", "Unknown"),
            "allocated_part": part_id,
            "quantity": quantity,
            "estimated_delivery_hours": estimated_hours,
            "logistics_status": "Route clear and verified"
        }

    def trigger_inventory_shortage_fallback(self, plant_id: str) -> Dict[str, Any]:
        """Triggers fallback lookup if local parts inventory is depleted."""
        alternatives = self.optimizer.find_alternative_suppliers(plant_id)
        if not alternatives:
            return {"status": "critical", "message": "No emergency backup suppliers trackable for this plant profile."}
            
        return {
            "status": "mitigated",
            "message": "Alternative sourcing locations verified successfully.",
            "backup_options": alternatives
        }
# Force Day 4 Order Processor Update Implementation

# Day 4: Processing verification update
