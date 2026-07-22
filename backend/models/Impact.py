# backend/models/impact.py
"""
Data models for Supply Chain Impact Analysis.
"""

from pydantic import BaseModel, ConfigDict, Field
from backend.models.enums import BusinessImpact, SeverityLevel
from backend.models.supply_chain import MatchedSupplier


class InventoryImpactDetails(BaseModel):
    """Detailed inventory status for an affected plant-material relationship."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    inventory_id: str = Field(..., description="Unique inventory record ID.")
    plant_id: str = Field(..., description="Plant ID where inventory is held.")
    material_id: str = Field(..., description="Material ID.")
    material_name: str = Field(..., description="Name of the material.")
    supplier_id: str | None = Field(default=None, description="Primary supplier ID.")
    available_stock_tons: float = Field(..., description="Currently available stock in tons.")
    daily_consumption_tons: float = Field(..., description="Daily consumption rate in tons.")
    remaining_operational_days: float = Field(..., description="Operational days of stock remaining.")
    inventory_status: str = Field(..., description="Inventory status (e.g. Critical, Low, Warning, Healthy).")
    criticality: str = Field(default="MEDIUM", description="Material criticality level.")


class PlantImpactDetails(BaseModel):
    """Detailed production impact for an affected manufacturing plant."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    plant_id: str = Field(..., description="Plant ID.")
    plant_name: str = Field(..., description="Plant name.")
    city: str | None = Field(default=None, description="City location.")
    state: str | None = Field(default=None, description="State location.")
    production_capacity_tpd: float = Field(..., description="Total production capacity in tons per day.")
    current_daily_production_tpd: float = Field(..., description="Current daily production in tons per day.")
    estimated_production_loss_tpd: float = Field(..., description="Estimated daily production loss in tons per day.")
    operating_status: str = Field(..., description="Current operating status of the plant.")


class ImpactAnalysis(BaseModel):
    """
    Structured impact analysis produced by the Supply Chain Impact Agent,
    ready for consumption by the Mitigation Planning Agent.
    """

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    affected_suppliers: list[MatchedSupplier | str] = Field(
        default_factory=list,
        description="List of suppliers directly or indirectly affected by the disruption.",
    )

    affected_materials: list[str] = Field(
        default_factory=list,
        description="List of materials affected by the disruption.",
    )

    affected_plants: list[str] = Field(
        default_factory=list,
        description="List of manufacturing plants impacted by the disruption.",
    )

    affected_warehouses: list[str] = Field(
        default_factory=list,
        description="List of warehouses affected by the disruption.",
    )

    affected_distribution_centers: list[str] = Field(
        default_factory=list,
        description="List of distribution centers impacted downstream.",
    )

    inventory_status: str = Field(
        ...,
        description="Summary of overall inventory risk status (e.g. Critical, High Risk, Moderate Risk, Healthy).",
    )

    estimated_inventory_remaining_days: float = Field(
        ...,
        description="Estimated operational days of inventory remaining before stockout (minimum across affected inventories).",
    )

    production_impact: str = Field(
        ...,
        description="Summary of production capacity at risk (e.g. TPD loss, percentage capacity affected).",
    )

    business_impact: BusinessImpact = Field(
        ...,
        description="Overall business impact level (low, medium, high, severe).",
    )

    supply_chain_blast_radius: str = Field(
        ...,
        description="Description of the overall blast radius across the network graph.",
    )

    overall_impact_severity: SeverityLevel = Field(
        ...,
        description="Overall impact severity level (low, medium, high, critical).",
    )

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for this impact analysis.",
    )

    # Detailed sub-breakdowns for downstream mitigation planning
    inventory_details: list[InventoryImpactDetails] = Field(
        default_factory=list,
        description="Breakdown of specific plant inventory items at risk.",
    )

    plant_details: list[PlantImpactDetails] = Field(
        default_factory=list,
        description="Breakdown of specific plant production impacts.",
    )
