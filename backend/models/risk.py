from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import (
    BusinessImpact,
    RiskCategory,
    SeverityLevel,
)


class AffectedEntity(BaseModel):
    """Represents a supplier or organization affected by the disruption."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    name: str = Field(
        ...,
        min_length=1,
        description="Name of the affected entity.",
    )

    entity_type: str = Field(
        ...,
        min_length=1,
        description="Type of entity (supplier, manufacturer, port, etc.).",
    )

    location: str | None = Field(
        default=None,
        description="Location of the affected entity.",
    )

    description: str | None = Field(
        default=None,
        description="Additional details about the affected entity.",
    )


class RiskAssessment(BaseModel):
    """Structured AI-generated supply chain risk assessment."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    category: RiskCategory = Field(
        ...,
        description="Primary disruption category.",
    )

    severity: SeverityLevel = Field(
        ...,
        description="Overall disruption severity.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    business_impact: BusinessImpact = Field(
        ...,
        description="Estimated business impact.",
    )

    affected_suppliers: list[AffectedEntity] = Field(
        default_factory=list,
        description="Affected suppliers or organizations.",
    )

    affected_materials: list[str] = Field(
        default_factory=list,
        description="Affected raw materials.",
    )

    summary: str = Field(
        ...,
        min_length=1,
        description="Executive summary of the disruption.",
    )

    reasoning: str = Field(
        ...,
        min_length=1,
        description="Reasoning behind the AI assessment.",
    )

    recommended_action: str = Field(
        ...,
        min_length=1,
        description="Recommended mitigation action.",
    )


class RiskAnalysis(BaseModel):
    """Complete AI risk analysis generated from a news article."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    news_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier of the news article.",
    )

    headline: str = Field(
        ...,
        min_length=1,
        description="Headline of the analyzed article.",
    )

    published_date: datetime = Field(
        ...,
        description="Publication date of the article.",
    )

    assessment: RiskAssessment = Field(
        ...,
        description="AI-generated risk assessment.",
    )