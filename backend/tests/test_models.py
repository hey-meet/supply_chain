import pytest
from datetime import datetime

from backend.models.news import NewsArticle
from backend.models.risk import RiskAssessment, RiskAnalysis
from backend.models.agent_response import AgentResponse
from backend.models.supply_chain import MatchedSupplier
from backend.models.enums import MatchReason, RiskCategory, SeverityLevel, BusinessImpact
from backend.models.news_filter import FilteredNewsCollection
from backend.models.executive_summary import ExecutiveSummary


def test_import_models():
    assert NewsArticle
    assert AgentResponse
    assert RiskAssessment
    assert RiskAnalysis
    assert MatchedSupplier
    assert FilteredNewsCollection
    assert ExecutiveSummary


def test_matched_supplier_validation():
    # Valid enum test
    supplier = MatchedSupplier(
        supplier_id="SUP-001",
        supplier_name="Acme Corp",
        match_reason=MatchReason.NAME
    )
    assert supplier.match_reason == MatchReason.NAME

    # String parsing (backward compatibility with string representation)
    supplier_str = MatchedSupplier(
        supplier_id="SUP-002",
        supplier_name="Global Tech",
        match_reason="location"
    )
    assert supplier_str.match_reason == MatchReason.LOCATION

    # Invalid enum test
    with pytest.raises(ValueError):
        MatchedSupplier(
            supplier_id="SUP-003",
            supplier_name="Bad Co",
            match_reason="invalid_reason"
        )


def test_risk_assessment_validation():
    assessment = RiskAssessment(
        category=RiskCategory.WEATHER,
        severity=SeverityLevel.HIGH,
        confidence=0.9,
        business_impact=BusinessImpact.HIGH,
        summary="Typhoon warning",
        reasoning="Weather API data",
        recommended_action="Stock up"
    )
    assert assessment.category == RiskCategory.WEATHER
    assert assessment.confidence == 0.9

    with pytest.raises(ValueError):
        # Invalid confidence (must be <= 1.0)
        RiskAssessment(
            category=RiskCategory.WEATHER,
            severity=SeverityLevel.HIGH,
            confidence=1.5,
            business_impact=BusinessImpact.HIGH,
            summary="Test",
            reasoning="Test",
            recommended_action="Test"
        )


def test_risk_analysis_validation():
    supplier = MatchedSupplier(
        supplier_id="SUP-001",
        supplier_name="Acme Corp",
        match_reason=MatchReason.NAME_AND_LOCATION
    )
    
    assessment = RiskAssessment(
        category=RiskCategory.WEATHER,
        severity=SeverityLevel.HIGH,
        confidence=0.9,
        business_impact=BusinessImpact.HIGH,
        summary="Typhoon",
        reasoning="Weather API data",
        recommended_action="Stock up"
    )
    
    analysis = RiskAnalysis(
        news_id="news-123",
        headline="Major Typhoon",
        published_date=datetime.now(),
        assessment=assessment,
        matched_suppliers=[supplier]
    )
    assert analysis.news_id == "news-123"
    assert len(analysis.matched_suppliers) == 1
    assert analysis.matched_suppliers[0].match_reason == MatchReason.NAME_AND_LOCATION
