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
