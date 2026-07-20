"""
test_knowledge_graph_agent.py

Tests for the Knowledge Graph Agent, run against the REAL data files
in backend/data/ (not mocked), since this agent's whole job is to
correctly represent that real data as a graph.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.agents.knowledge_graph_agent import KnowledgeGraphAgent


def _build_agent() -> KnowledgeGraphAgent:
    return KnowledgeGraphAgent()


# -----------------------------------------------------------------------
# Graph construction
# -----------------------------------------------------------------------
def test_graph_builds_expected_node_counts():
    agent = _build_agent()
    summary = agent.summary()

    assert summary["node_counts"]["plant"] == 3
    assert summary["node_counts"]["supplier"] == 5
    assert summary["node_counts"]["warehouse"] == 3
    assert summary["node_counts"]["distribution_center"] == 3
    assert summary["node_counts"]["material"] == 6
    assert summary["total_nodes"] == 20


def test_graph_has_edges():
    agent = _build_agent()
    summary = agent.summary()
    assert summary["total_edges"] > 0

# -----------------------------------------------------------------------
# Node info
# -----------------------------------------------------------------------
def test_get_node_info_returns_supplier_details():
    agent = _build_agent()
    info = agent.get_node_info("SUP-001")

    assert info is not None
    assert info["node_type"] == "supplier"
    assert info["name"] == "Marwar Mining & Minerals Corp."
    assert info["state"] == "Rajasthan"


def test_get_node_info_returns_none_for_unknown_node():
    agent = _build_agent()
    assert agent.get_node_info("NOT-A-REAL-NODE") is None


# -----------------------------------------------------------------------
# Material <-> supplier relationships
# -----------------------------------------------------------------------
def test_get_suppliers_of_material_returns_primary_and_backup():
    agent = _build_agent()
    suppliers = agent.get_suppliers_of_material("MAT-LMS-01")

    supplier_ids = {s["supplier_id"] for s in suppliers}
    assert supplier_ids == {"SUP-001", "SUP-002"}

    roles = {s["supplier_id"]: s["role"] for s in suppliers}
    assert roles["SUP-001"] == "primary"
    assert roles["SUP-002"] == "backup"


def test_get_materials_supplied_by_supplier():
    agent = _build_agent()
    materials = agent.get_materials_supplied_by("SUP-001")
    assert set(materials) == {"MAT-LMS-01", "MAT-COL-02"}

# -----------------------------------------------------------------------
# Supplier <-> plant relationships
# -----------------------------------------------------------------------
def test_get_plants_supplied_by_marks_primary_and_secondary_roles():
    agent = _build_agent()
    plants = agent.get_plants_supplied_by("SUP-001")

    plants_by_id = {p["plant_id"]: p["role"] for p in plants}
    assert plants_by_id["PLT-001"] == "primary"
    assert plants_by_id["PLT-002"] == "secondary"


# -----------------------------------------------------------------------
# Warehouse <-> plant relationships
# -----------------------------------------------------------------------
def test_get_plants_fed_by_warehouse():
    agent = _build_agent()
    plants = agent.get_plants_fed_by_warehouse("RWH-002")
    assert set(plants) == {"PLT-001", "PLT-002"}


# -----------------------------------------------------------------------
# Plant <-> distribution center relationships
# -----------------------------------------------------------------------
def test_get_distribution_centers_for_plant():
    agent = _build_agent()
    centers = agent.get_distribution_centers_for_plant("PLT-001")
    assert centers == ["DBC-001"]


# -----------------------------------------------------------------------
# The "blast radius" query — the whole point of this agent
# -----------------------------------------------------------------------
def test_downstream_impact_from_disrupted_supplier():
    agent = _build_agent()
    impact = agent.get_downstream_impact("SUP-001")

    # SUP-001 supplies limestone + coal, feeds PLT-001 (primary) and
    # PLT-002 (secondary), which distribute to DBC-001 and DBC-002.
    assert set(impact["material"]) == {"MAT-LMS-01", "MAT-COL-02"}
    assert set(impact["plant"]) == {"PLT-001", "PLT-002"}
    assert set(impact["distribution_center"]) == {"DBC-001", "DBC-002"}


def test_downstream_impact_from_unknown_node_returns_empty():
    agent = _build_agent()
    assert agent.get_downstream_impact("NOT-A-REAL-NODE") == {}


if __name__ == "__main__":
    test_functions = [
        test_graph_builds_expected_node_counts,
        test_graph_has_edges,
        test_get_node_info_returns_supplier_details,
        test_get_node_info_returns_none_for_unknown_node,
        test_get_suppliers_of_material_returns_primary_and_backup,
        test_get_materials_supplied_by_supplier,
        test_get_plants_supplied_by_marks_primary_and_secondary_roles,
        test_get_plants_fed_by_warehouse,
        test_get_distribution_centers_for_plant,
        test_downstream_impact_from_disrupted_supplier,
        test_downstream_impact_from_unknown_node_returns_empty,
    ]
    for test_fn in test_functions:
        test_fn()
        print("PASS:", test_fn.__name__)
    print("All tests passed!")
