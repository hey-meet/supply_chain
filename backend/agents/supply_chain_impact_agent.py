# backend/agents/supply_chain_impact_agent.py
"""
Supply Chain Impact Agent: The main business reasoning agent in the pipeline.

Inputs:
  - RiskAssessment (or RiskAnalysis)
  - KnowledgeGraphAgent
  - Inventory data
  - Plant data
  - Supplier data

Output:
  - ImpactAnalysis (structured Pydantic object)
"""

import json
import logging
from pathlib import Path
from typing import Any

from backend.agents.knowledge_graph_agent import KnowledgeGraphAgent, knowledge_graph_agent
from backend.models.enums import BusinessImpact, SeverityLevel
from backend.models.impact import ImpactAnalysis, InventoryImpactDetails, PlantImpactDetails
from backend.models.risk import RiskAnalysis, RiskAssessment
from backend.models.supply_chain import MatchedSupplier

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class SupplyChainImpactAgent:
    """
    Main business reasoning agent that calculates downstream impact,
    remaining operational inventory days, production loss (TPD), and total blast radius.
    """

    def __init__(
        self,
        kg_agent: KnowledgeGraphAgent | None = None,
        data_dir: Path = DATA_DIR,
    ):
        self.kg_agent = kg_agent or knowledge_graph_agent
        self.data_dir = data_dir
        self.inventory_data = self._load_json("inventory/inventory.json").get("plant_inventories", [])
        self.plants_data = self._load_json("plants/plants.json").get("plants", [])
        self.suppliers_data = self._load_json("suppliers/suppliers.json").get("suppliers", [])
        self.warehouses_data = self._load_json("warehouses/warehouses.json").get("warehouses", [])
        self.distribution_data = self._load_json("distribution/distribution_centers.json").get(
            "distribution_centers", []
        )

    def _load_json(self, relative_path: str) -> dict:
        """Loads a JSON file relative to the data directory."""
        full_path = self.data_dir / relative_path
        if not full_path.exists():
            logger.warning("Data file not found: %s", full_path)
            return {}
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("Error loading JSON file %s: %s", full_path, exc)
            return {}
