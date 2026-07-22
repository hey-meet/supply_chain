from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import BusinessImpact, SeverityLevel
from backend.models.risk import RiskAnalysis


class InventoryImpact(BaseModel):
    """Represents inventory availability for an affected plant."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    plant_id: str

    material: str

    current_stock_days: float = Field(
        ...,
        ge=0,
        description="Estimated inventory remaining in days.",
    )

    status: str = Field(
        ...,
        description="safe | warning | critical",
    )


class PlantImpact(BaseModel):
    """Operational impact on a manufacturing plant."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    plant_id: str

    plant_name: str

    affected_materials: list[str] = Field(default_factory=list)

    affected_suppliers: list[str] = Field(default_factory=list)

    production_loss_percent: float = Field(
        default=0.0,
        ge=0,
        le=100,
    )


class ImpactAnalysis(BaseModel):
    """Operational impact generated after risk assessment."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    risk: RiskAnalysis

    affected_plants: list[PlantImpact] = Field(
        default_factory=list,
    )

    affected_warehouses: list[str] = Field(
        default_factory=list,
    )

    affected_distribution_centers: list[str] = Field(
        default_factory=list,
    )

    inventory: list[InventoryImpact] = Field(
        default_factory=list,
    )

    alternate_suppliers: list[str] = Field(
        default_factory=list,
    )

    dependency_chain: list[dict] = Field(
        default_factory=list,
    )

    overall_business_impact: BusinessImpact

    overall_severity: SeverityLevel

    estimated_production_loss_percent: float = Field(
        default=0.0,
        ge=0,
        le=100,
    )

    reasoning: str