# backend/tests/test_supply_chain_impact_agent.py
"""
Unit tests for SupplyChainImpactAgent.
"""

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.agents.supply_chain_impact_agent import SupplyChainImpactAgent
from backend.models.enums import BusinessImpact, MatchReason, RiskCategory, SeverityLevel
from backend.models.impact import ImpactAnalysis
from backend.models.risk import AffectedEntity, RiskAssessment
from backend.models.supply_chain import MatchedSupplier


def get_sample_risk_assessment() -> RiskAssessment:
    return RiskAssessment(
        category=RiskCategory.RAW_MATERIAL_SHORTAGE,
        severity=SeverityLevel.HIGH,
        confidence=0.9,
        business_impact=BusinessImpact.HIGH,
        affected_suppliers=[
            AffectedEntity(
                name="Marwar Mining & Minerals Corp.",
                entity_type="supplier",
                location="Jodhpur, Rajasthan",
            )
        ],
        affected_materials=["MAT-LMS-01", "Coal"],
        summary="Severe flooding and heavy rainfall disrupted coal and limestone mining operations.",
        reasoning="Flooding prevented mining transport trucks from leaving Jodhpur mines.",
        recommended_action="Activate backup limestone suppliers and reroute coal via rail.",
    )


def get_sample_matched_suppliers() -> list[MatchedSupplier]:
    return [
        MatchedSupplier(
            supplier_id="SUP-001",
            supplier_name="Marwar Mining & Minerals Corp.",
            city="Jodhpur",
            state="Rajasthan",
            country="India",
            materials=["MAT-LMS-01", "MAT-COL-02"],
            reliability_score=94.5,
            business_priority="High",
            match_reason=MatchReason.NAME_AND_LOCATION,
        )
    ]

@pytest.fixture
def sample_risk_assessment():
    return get_sample_risk_assessment()


@pytest.fixture
def sample_matched_suppliers():
    return get_sample_matched_suppliers()


def test_agent_initialization():
    agent = SupplyChainImpactAgent()
    assert agent.inventory_data is not None
    assert agent.plants_data is not None
    assert agent.suppliers_data is not None
    assert agent.kg_agent is not None


def test_analyze_impact(sample_risk_assessment, sample_matched_suppliers):
    agent = SupplyChainImpactAgent()
    analysis = agent.analyze_impact(
        assessment_input=sample_risk_assessment,
        matched_suppliers=sample_matched_suppliers,
    )

    assert isinstance(analysis, ImpactAnalysis)

    # Check affected entities
    assert len(analysis.affected_suppliers) >= 1
    assert "MAT-LMS-01" in analysis.affected_materials or len(analysis.affected_materials) > 0
    assert len(analysis.affected_plants) > 0

    # Check numerical calculations
    assert analysis.estimated_inventory_remaining_days > 0
    assert analysis.confidence_score >= 0.8
    assert "Blast Radius" in analysis.supply_chain_blast_radius
    assert analysis.business_impact in [BusinessImpact.HIGH, BusinessImpact.SEVERE]

def test_agent_question_answering_helpers(sample_risk_assessment, sample_matched_suppliers):
    agent = SupplyChainImpactAgent()
    analysis = agent.analyze_impact(
        assessment_input=sample_risk_assessment,
        matched_suppliers=sample_matched_suppliers,
    )

    suppliers = agent.get_affected_suppliers(analysis)
    assert len(suppliers) > 0
    assert any("Marwar Mining" in s or "SUP-001" in s for s in suppliers)

    materials = agent.get_affected_materials(analysis)
    assert isinstance(materials, list)

    plants = agent.get_affected_plants(analysis)
    assert len(plants) > 0

    warehouses = agent.get_affected_warehouses(analysis)
    assert isinstance(warehouses, list)

    dcs = agent.get_affected_distribution_centers(analysis)
    assert isinstance(dcs, list)

    inv_risk = agent.get_inventory_at_risk(analysis)
    assert isinstance(inv_risk, list)

    rem_days = agent.get_remaining_operational_days(analysis)
    assert isinstance(rem_days, float)

    prod_loss = agent.get_estimated_production_loss(analysis)
    assert "TPD" in prod_loss or "capacity" in prod_loss

    biz_impact = agent.get_business_impact(analysis)
    assert biz_impact in ["high", "severe", "medium", "low"]

    blast_radius = agent.get_blast_radius(analysis)
    assert "Blast Radius" in blast_radius


if __name__ == "__main__":
    print("Running SupplyChainImpactAgent tests...")
    test_agent_initialization()
    assessment = get_sample_risk_assessment()
    suppliers = get_sample_matched_suppliers()
    test_analyze_impact(assessment, suppliers)
    test_agent_question_answering_helpers(assessment, suppliers)
    print("All SupplyChainImpactAgent tests passed successfully!")
