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
 
