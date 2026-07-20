"""
knowledge_graph_agent.py
 
The Knowledge Graph Agent: builds and queries a graph representation of
the ENTIRE physical supply chain network — suppliers, materials,
plants, warehouses, and distribution centers — and how they connect.
"""
import json
import logging
from pathlib import Path

import networkx as nx

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MANIFEST_FILE = DATA_DIR / "data_manifest.json"

FALLBACK_MATERIAL_NAMES = {
    "MAT-LMS-01": "Limestone",
    "MAT-COL-02": "Coal",
    "MAT-GYP-03": "Gypsum",
    "MAT-FLA-04": "Fly Ash",
    "MAT-DSL-05": "Diesel",
    "MAT-PKG-06": "Packaging Material",
}

class KnowledgeGraphAgent:
    """
    Builds a NetworkX graph of the supply chain network and provides
    simple, reusable query methods on top of it.
 
    Node types (stored as node attribute "node_type"):
        "supplier", "material", "plant", "warehouse", "distribution_center"
 
    Edge types (stored as edge attribute "relation"):
        "SUPPLIES_MATERIAL"   supplier -> material
        "SUPPLIES_PLANT"      supplier -> plant
        "FEEDS_PLANT"         warehouse -> plant
        "DISTRIBUTES_TO"      plant -> distribution_center
    """
 
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.graph = nx.DiGraph()
        self._build_graph()
 
    # ---------------------------------------------------------------
    # STEP 1: Loading raw JSON files
    # ---------------------------------------------------------------
    def _load_json(self, relative_path: str) -> dict:
        """
        Loads one JSON file, given a path relative to backend/data/
        (matching the style used in data_manifest.json).
 
        Returns an empty dict if the file doesn't exist, so a single
        missing file doesn't crash the whole graph build — we just log
        a warning and build the graph with whatever data IS available.
        """
        full_path = self.data_dir / relative_path
 
        if not full_path.exists():
            logger.warning("Data file not found, skipping: %s", full_path)
            return {}
 
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---------------------------------------------------------------
    # STEP 2: Build every node first, then every edge
    # ---------------------------------------------------------------
    def _build_graph(self) -> None:
        """Loads all the data files and builds the full graph."""
        company = self._load_json("company/company.json")
        plants_data = self._load_json("plants/plants.json").get("plants", [])
        suppliers_data = self._load_json("suppliers/suppliers.json").get("suppliers", [])
        warehouses_data = self._load_json("warehouses/warehouses.json").get("warehouses", [])
        distribution_data = self._load_json("distribution/distribution_centers.json").get(
            "distribution_centers", []
        )
 
        material_supplier_map = self._load_json(
            "relationships/material_supplier_map.json"
        ).get("material_supplier_mappings", [])
        plant_supplier_map = self._load_json(
            "relationships/plant_supplier_map.json"
        ).get("plant_supplier_mappings", [])
        warehouse_plant_map = self._load_json(
            "relationships/warehouse_plant_map.json"
        ).get("warehouse_plant_mappings", [])
        plant_distribution_map = self._load_json(
            "relationships/plant_distribution_map.json"
        ).get("plant_distribution_mappings", [])
 
        # Keep the company record around for reference (not a graph
        # node — there's only one company, no relationships to model).
        self.company = company
 
        # --- Nodes ---
        self._add_plant_nodes(plants_data)
        self._add_supplier_nodes(suppliers_data)
        self._add_warehouse_nodes(warehouses_data)
        self._add_distribution_center_nodes(distribution_data)
        self._add_material_nodes(material_supplier_map)
 
        # --- Edges ---
        self._add_material_supplier_edges(material_supplier_map)
        self._add_plant_supplier_edges(plant_supplier_map)
        self._add_warehouse_plant_edges(warehouse_plant_map)
        self._add_plant_distribution_edges(plant_distribution_map)
     
    def _add_plant_nodes(self, plants_data: list[dict]) -> None:
        for plant in plants_data:
            self.graph.add_node(
                plant["plant_id"],
                node_type="plant",
                name=plant.get("plant_name"),
                city=plant.get("city"),
                state=plant.get("state"),
                production_capacity_tpd=plant.get("production_capacity_tpd"),
                storage_capacity_tons=plant.get("storage_capacity_tons"),
                risk_zone=plant.get("risk_zone"),
                operating_status=plant.get("operating_status"),
            )
 
    def _add_supplier_nodes(self, suppliers_data: list[dict]) -> None:
        for supplier in suppliers_data:
            self.graph.add_node(
                supplier["supplier_id"],
                node_type="supplier",
                name=supplier.get("supplier_name"),
                city=supplier.get("city"),
                state=supplier.get("state"),
                country=supplier.get("country"),
                reliability_score=supplier.get("reliability_score"),
                business_priority=supplier.get("business_priority"),
                lead_time_days=supplier.get("lead_time_days"),
                preferred_transport=supplier.get("preferred_transport"),
                status=supplier.get("status"),
            )

    def _add_warehouse_nodes(self, warehouses_data: list[dict]) -> None:
        for warehouse in warehouses_data:
            self.graph.add_node(
                warehouse["warehouse_id"],
                node_type="warehouse",
                name=warehouse.get("warehouse_name"),
                city=warehouse.get("city"),
                state=warehouse.get("state"),
                storage_capacity_tons=warehouse.get("storage_capacity_tons"),
                current_utilization_tons=warehouse.get("current_utilization_tons"),
                operating_status=warehouse.get("operating_status"),
            )

    def _add_distribution_center_nodes(self, distribution_data: list[dict]) -> None:
        for center in distribution_data:
            self.graph.add_node(
                center["distribution_center_id"],
                node_type="distribution_center",
                name=center.get("distribution_center_name"),
                city=center.get("city"),
                state=center.get("state"),
                supported_regions=center.get("supported_regions", []),
                operating_status=center.get("operating_status"),
            )

    def _add_material_nodes(self, material_supplier_map: list[dict]) -> None:
        """
        Adds one node per material ID found in material_supplier_map.
        Since materials/materials.json doesn't exist yet, we use a
        fallback name lookup (see _FALLBACK_MATERIAL_NAMES) — if that
        file is added later, this should read the real names from it
        instead.
        """
        for mapping in material_supplier_map:
            material_id = mapping["material_id"]
            self.graph.add_node(
                material_id,
                node_type="material",
                name=FALLBACK_MATERIAL_NAMES.get(material_id, material_id),
                criticality=mapping.get("criticality"),
                average_monthly_requirement=mapping.get("average_monthly_requirement"),
            )
