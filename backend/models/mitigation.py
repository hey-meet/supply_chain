from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import SeverityLevel


class AlternateSupplier(BaseModel):
    """Recommended alternate supplier."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    supplier_id: str

    supplier_name: str

    supplied_materials: list[str] = Field(
        default_factory=list,
    )

    reason: str


class TransportRecommendation(BaseModel):
    """Recommended transportation alternative."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    mode: str = Field(
        ...,
        description="Road, Rail, Port, Air, etc.",
    )

    description: str


class InventoryRecommendation(BaseModel):
    """Inventory mitigation recommendation."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    plant_id: str

    action: str

    priority: str = Field(
        ...,
        description="Low | Medium | High | Critical",
    )


class ProductionRecommendation(BaseModel):
    """Production planning recommendation."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    affected_plant: str

    recommendation: str


class MitigationAction(BaseModel):
    """Individual mitigation action."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    title: str

    description: str

    priority: str = Field(
        ...,
        description="Low | Medium | High | Critical",
    )

    estimated_duration: str


class MitigationPlan(BaseModel):
    """Enterprise mitigation strategy generated from ImpactAnalysis."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    alternate_suppliers: list[AlternateSupplier] = Field(
        default_factory=list,
    )

    transportation_plan: list[TransportRecommendation] = Field(
        default_factory=list,
    )

    inventory_plan: list[InventoryRecommendation] = Field(
        default_factory=list,
    )

    production_plan: list[ProductionRecommendation] = Field(
        default_factory=list,
    )

    actions: list[MitigationAction] = Field(
        default_factory=list,
    )

    executive_recommendation: str

    recovery_estimate: str

    estimated_cost: str | None = None

    overall_priority: SeverityLevel