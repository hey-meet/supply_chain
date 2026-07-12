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
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get_all_assets(self) -> Dict[str, Any]:
        return self.data

    def get_plant_by_id(self, plant_id: str) -> Optional[Dict[str, Any]]:
        return next((p for p in self.data.get("production_plants", []) if p["plant_id"] == plant_id), None)

kb_manager = KnowledgeBaseManager()