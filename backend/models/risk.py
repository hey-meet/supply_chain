from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RiskCategory(str, Enum):
    """Supported supply chain disruption categories."""

    RAW_MATERIAL_SHORTAGE = "RAW_MATERIAL_SHORTAGE"
    TRANSPORTATION = "TRANSPORTATION"
    WEATHER = "WEATHER"
    PORT_CONGESTION = "PORT_CONGESTION"
    SUPPLIER_FAILURE = "SUPPLIER_FAILURE"
    REGULATORY = "REGULATORY"
    LABOR_STRIKE = "LABOR_STRIKE"
    ENERGY = "ENERGY"
    PRICE_FLUCTUATION = "PRICE_FLUCTUATION"
    GEOPOLITICAL = "GEOPOLITICAL"
    OTHER = "OTHER"


class RiskSeverity(str, Enum):
    """Overall severity level of the disruption."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BusinessImpact(str, Enum):
    """Estimated business impact."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    SEVERE = "SEVERE"


class AffectedEntity(BaseModel):
    """Represents a supplier or organization affected by the disruption."""

    name: str
    entity_type: str
    location: str | None = None
    description: str | None = None


class RiskAssessment(BaseModel):
    """Structured AI-generated supply chain risk assessment."""

    category: RiskCategory
    severity: RiskSeverity
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )
    business_impact: BusinessImpact

    affected_suppliers: list[AffectedEntity] = Field(default_factory=list)
    affected_materials: list[str] = Field(default_factory=list)

    summary: str
    reasoning: str
    recommended_action: str


class RiskAnalysis(BaseModel):
    """Complete AI risk analysis generated from a news article."""

    news_id: str
    headline: str
    published_date: datetime
    assessment: RiskAssessment