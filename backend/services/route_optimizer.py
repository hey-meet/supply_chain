import os
import sys
from typing import Dict, Any, List, Optional

# Ensure the backend directory is in the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.manager import kb_manager

class RouteOptimizerService:
    def __init__(self):
        self.kb = kb_manager

    def validate_route(self, route_id: str) -> Dict[str, Any]:
        """Check if a transportation route exists and return its operational status."""
        route = self.kb.get_route_by_id(route_id)
        if not route:
            return {"status": "error", "message": f"Route ID {route_id} not found in knowledge base."}
        
        # Simple validation rule
        is_active = route.get("status", "Active") == "Active"
        return {
            "status": "success",
            "route_id": route_id,
            "is_operable": is_active,
            "details": route
        }

    def calculate_estimated_delay(self, route_id: str, weather_factor: float = 1.0) -> Optional[float]:
        """Calculate transit delay multiplier based on route conditions."""
        route = self.kb.get_route_by_id(route_id)
        if not route:
            return None
        
        base_time = route.get("transit_time_hours", 24.0)
        # Apply logic factor
        return round(base_time * weather_factor, 2)

    def find_alternative_suppliers(self, critical_plant_id: str) -> List[Dict[str, Any]]:
        """Find suppliers capable of servicing a given production plant."""
        plant = self.kb.get_plant_by_id(critical_plant_id)
        if not plant:
            return []
            
        required_materials = plant.get("required_inputs", [])
        all_assets = self.kb.get_all_assets()
        suppliers = all_assets.get("suppliers", [])
        
        alternatives = []
        for supplier in suppliers:
            # Check if supplier offers any of the materials the plant needs
            supplied_materials = supplier.get("materials_supplied", [])
            matches = list(set(required_materials).intersection(set(supplied_materials)))
            if matches:
                alternatives.append({
                    "supplier_id": supplier.get("supplier_id"),
                    "name": supplier.get("name"),
                    "matching_materials": matches
                })
        return alternatives