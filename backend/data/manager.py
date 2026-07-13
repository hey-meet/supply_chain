import os
import json
from typing import Dict, Any, Optional

class KnowledgeBaseManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "knowledge_base.json")
        self.data: Dict[str, Any] = self._load_database()

    def _load_database(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {"production_plants": [], "suppliers": [], "warehouses": [], "transportation_routes": []}
        
        # FIX 1: Explicitly added encoding="utf-8" as requested by Meet
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        # FIX 2: Added error handling robust check for invalid JSON
        except json.JSONDecodeError:
            print(f"Error: {self.file_path} contains invalid JSON formatting.")
            return {"production_plants": [], "suppliers": [], "warehouses": [], "transportation_routes": []}

    def get_all_assets(self) -> Dict[str, Any]:
        return self.data

    def get_plant_by_id(self, plant_id: str) -> Optional[Dict[str, Any]]:
        return next((p for p in self.data.get("production_plants", []) if p["plant_id"] == plant_id), None)

    # FIX 3: Added consistent lookup method for Suppliers
    def get_supplier_by_id(self, supplier_id: str) -> Optional[Dict[str, Any]]:
        return next((s for s in self.data.get("suppliers", []) if s["supplier_id"] == supplier_id), None)

    # FIX 3: Added consistent lookup method for Warehouses
    def get_warehouse_by_id(self, warehouse_id: str) -> Optional[Dict[str, Any]]:
        return next((w for w in self.data.get("warehouses", []) if w["warehouse_id"] == warehouse_id), None)

    # FIX 3: Added consistent lookup method for Transportation Routes
    def get_route_by_id(self, route_id: str) -> Optional[Dict[str, Any]]:
        return next((r for r in self.data.get("transportation_routes", []) if r["route_id"] == route_id), None)

kb_manager = KnowledgeBaseManager()