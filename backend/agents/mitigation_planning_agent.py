
"""
Mitigation Planning Agent module for Cement Manufacturing Autonomous Monitoring.

This module consumes ImpactAnalysis domain models produced by the SupplyChainImpactAgent
and applies deterministic enterprise business rules to generate a comprehensive, actionable
MitigationPlan. It converts high-level risk and operational impact evaluations into concrete
mitigation steps, inventory rebalancing recommendations, transportation alternatives, and cost
or recovery estimates without using external LLM services.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set

from backend.models.enums import SeverityLevel
from backend.models.impact import ImpactAnalysis, InventoryImpact, PlantImpact
from backend.models.mitigation import (
    AlternateSupplier,
    InventoryRecommendation,
    MitigationAction,
    MitigationPlan,
    ProductionRecommendation,
    TransportRecommendation,
)

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURABLE CONSTANTS & THRESHOLDS
# ============================================================================

# Stock days thresholds
STOCK_THRESHOLD_CRITICAL = 2.0
STOCK_THRESHOLD_HIGH = 5.0
STOCK_THRESHOLD_MEDIUM = 10.0

# Production loss percentage thresholds
LOSS_THRESHOLD_HIGH = 50.0
LOSS_THRESHOLD_MEDIUM = 20.0
LOSS_THRESHOLD_LOW = 10.0

# Cost estimation loss percentage thresholds
COST_THRESHOLD_VERY_HIGH = 60.0
COST_THRESHOLD_HIGH = 30.0
COST_THRESHOLD_MEDIUM = 10.0


class MitigationPlanningAgent:
    """
    Agent responsible for translating supply chain impact analysis into a structured,
    deterministic mitigation plan for enterprise cement manufacturing operations.
    """

    def __init__(self) -> None:
        """Initialize the MitigationPlanningAgent."""
        logger.info("Initializing MitigationPlanningAgent.")

    def analyze(self, impact_analysis: ImpactAnalysis) -> MitigationPlan:
        """
        Main public entrypoint: Converts ImpactAnalysis into a deterministic MitigationPlan.

        :param impact_analysis: Fully constructed ImpactAnalysis Pydantic model.
        :return: Fully populated MitigationPlan Pydantic model.
        """
        logger.info("Generating enterprise mitigation plan from impact analysis.")

        try:
            alternate_suppliers = self._generate_alternate_suppliers(impact_analysis)
            transport_plan = self._generate_transport_plan(impact_analysis)
            inventory_plan = self._generate_inventory_plan(impact_analysis)
            production_plan = self._generate_production_plan(impact_analysis)
            actions = self._generate_actions(impact_analysis, inventory_plan, alternate_suppliers)
            summary = self._generate_summary(impact_analysis)
            executive_rec = self._generate_executive_recommendation(impact_analysis)
            recovery_est = self._estimate_recovery(impact_analysis)
            cost_est = self._estimate_cost(impact_analysis)

            return self._build_result(
                alternate_suppliers=alternate_suppliers,
                transport_plan=transport_plan,
                inventory_plan=inventory_plan,
                production_plan=production_plan,
                actions=actions,
                summary=summary,
                executive_rec=executive_rec,
                recovery_est=recovery_est,
                cost_est=cost_est,
                overall_priority=impact_analysis.overall_severity,
            )
        except Exception as err:
            logger.error(f"Error executing mitigation planning analysis: {err}", exc_info=True)
            return self._build_fallback_result(impact_analysis)

    def _generate_alternate_suppliers(
        self, impact_analysis: ImpactAnalysis
    ) -> List[AlternateSupplier]:
        """Convert raw alternate supplier strings or graph inputs into AlternateSupplier models."""
        results: List[AlternateSupplier] = []
        raw_alternates = impact_analysis.alternate_suppliers or []
        seen_ids: Set[str] = set()

        for alt in raw_alternates:
            supplier_id = ""
            supplier_name = ""

            if isinstance(alt, str):
                supplier_id = alt.lower().replace(" ", "_")
                supplier_name = alt
            elif isinstance(alt, dict):
                supplier_id = str(alt.get("supplier_id") or alt.get("id") or "alt_sup")
                supplier_name = str(alt.get("supplier_name") or supplier_id)

            if not supplier_id or supplier_id in seen_ids:
                continue

            seen_ids.add(supplier_id)

            results.append(
                AlternateSupplier(
                    supplier_id=supplier_id,
                    supplier_name=supplier_name,
                    supplied_materials=[],
                    reason="Recommended based on Supply Chain Knowledge Graph and material availability map.",
                )
            )

        return results

    def _generate_transport_plan(
        self, impact_analysis: ImpactAnalysis
    ) -> List[TransportRecommendation]:
        """Generate deterministic transport routing recommendations based on risk and operational scope."""
        recommendations: List[TransportRecommendation] = []
        severity = impact_analysis.overall_severity

        if severity == SeverityLevel.CRITICAL:
            recommendations.append(
                TransportRecommendation(
                    mode="Rail",
                    description="Reroute critical material shipments to high-capacity rail corridors to bypass regional road constraints.",
                )
            )
            recommendations.append(
                TransportRecommendation(
                    mode="Road",
                    description="Deploy expedited dedicated fleet trucks for short-haul transfers between unaffected regional warehouses.",
                )
            )
        elif severity == SeverityLevel.HIGH:
            recommendations.append(
                TransportRecommendation(
                    mode="Rail",
                    description="Shift bulk raw material transport to priority freight rail schedules.",
                )
            )
            recommendations.append(
                TransportRecommendation(
                    mode="Road",
                    description="Establish secondary trucking routes avoiding primary disrupted transport nodes.",
                )
            )
        else:
            recommendations.append(
                TransportRecommendation(
                    mode="Road",
                    description="Maintain standard motor carrier logistics with increased tracking frequency at key checkpoints.",
                )
            )

        if impact_analysis.affected_warehouses:
            recommendations.append(
                TransportRecommendation(
                    mode="Warehouse Logistics",
                    description=f"Route incoming deliveries via alternative active hubs: {', '.join(impact_analysis.affected_warehouses[:3])}.",
                )
            )

        return recommendations[:3]

    def _generate_inventory_plan(
        self, impact_analysis: ImpactAnalysis
    ) -> List[InventoryRecommendation]:
        """Generate plant-specific inventory actions based on stock depletion days."""
        recommendations: List[InventoryRecommendation] = []
        inventory_items = impact_analysis.inventory or []

        for inv in inventory_items:
            days = inv.current_stock_days
            plant_id = inv.plant_id or "UNKNOWN_PLANT"
            material = inv.material or "raw materials"

            if days < STOCK_THRESHOLD_CRITICAL:
                priority = SeverityLevel.CRITICAL
                action = f"Immediate emergency replenishment required for {material}. Initiate inter-plant stock transfer."
            elif days < STOCK_THRESHOLD_HIGH:
                priority = SeverityLevel.HIGH
                action = f"Expedite purchase order fulfillment for {material} and draw down safety stock reserves."
            elif days < STOCK_THRESHOLD_MEDIUM:
                priority = SeverityLevel.MEDIUM
                action = f"Schedule reorder for {material} and optimize daily consumption rates."
            else:
                priority = SeverityLevel.LOW
                action = f"Monitor stock levels for {material}. Regular supply buffer is sufficient."

            recommendations.append(
                InventoryRecommendation(
                    plant_id=plant_id,
                    action=action,
                    priority=priority,
                )
            )

        return recommendations

    def _generate_production_plan(
        self, impact_analysis: ImpactAnalysis
    ) -> List[ProductionRecommendation]:
        """Generate production adjustments for affected plants based on estimated capacity losses."""
        recommendations: List[ProductionRecommendation] = []
        plants = impact_analysis.affected_plants or []

        for plant in plants:
            loss_pct = plant.production_loss_percent
            plant_name = plant.plant_name or plant.plant_id

            if loss_pct > LOSS_THRESHOLD_HIGH:
                rec = f"Reduce daily kiln output by {loss_pct:.1f}%. Activate alternate raw material sourcing and shift non-urgent grinding schedules."
            elif loss_pct >= LOSS_THRESHOLD_MEDIUM:
                rec = f"Optimize batch scheduling to accommodate a {loss_pct:.1f}% material deficit. Prioritize high-margin cement blends."
            else:
                rec = f"Continue standard manufacturing operations while monitoring input feed rates for minor impacts ({loss_pct:.1f}% loss)."

            recommendations.append(
                ProductionRecommendation(
                    affected_plant=plant_name,
                    recommendation=rec,
                )
            )

        return recommendations

    def _generate_actions(
        self,
        impact_analysis: ImpactAnalysis,
        inventory_plan: List[InventoryRecommendation],
        alternate_suppliers: List[AlternateSupplier],
    ) -> List[MitigationAction]:
        """Generate a prioritized task list of concrete mitigation actions."""
        actions: List[MitigationAction] = []
        severity = impact_analysis.overall_severity

        if alternate_suppliers:
            sup_names = ", ".join([s.supplier_name for s in alternate_suppliers[:2]])
            actions.append(
                MitigationAction(
                    title="Engage Alternate Suppliers",
                    description=f"Initiate procurement contracts with secondary suppliers ({sup_names}) to fill material deficit.",
                    priority=SeverityLevel.HIGH if severity in (SeverityLevel.CRITICAL, SeverityLevel.HIGH) else SeverityLevel.MEDIUM,
                    estimated_duration="24 Hours",
                )
            )

        has_critical_inv = any(item.priority == SeverityLevel.CRITICAL for item in inventory_plan)
        if has_critical_inv:
            actions.append(
                MitigationAction(
                    title="Emergency Inventory Rebalancing",
                    description="Execute immediate inter-plant transfers from surplus facilities to critical stock locations.",
                    priority=SeverityLevel.CRITICAL,
                    estimated_duration="4 Hours",
                )
            )

        actions.append(
            MitigationAction(
                title="Logistics Corridor Optimization",
                description="Reroute critical freight shipments through unaffected transport pathways.",
                priority=SeverityLevel.MEDIUM if severity != SeverityLevel.CRITICAL else SeverityLevel.HIGH,
                estimated_duration="12 Hours",
            )
        )

        actions.append(
            MitigationAction(
                title="Executive Operations Review",
                description="Brief plant directors and supply chain committee on operational mitigation strategy.",
                priority=SeverityLevel.LOW if severity == SeverityLevel.LOW else SeverityLevel.MEDIUM,
                estimated_duration="Immediate",
            )
        )

        return actions

    def _generate_summary(self, impact_analysis: ImpactAnalysis) -> str:
        """Construct a multi-sentence executive summary of the mitigation strategy."""
        num_plants = len(impact_analysis.affected_plants or [])
        plant_str = f"{num_plants} manufacturing facility{'ies' if num_plants != 1 else ''}"
        severity = impact_analysis.overall_severity.value
        loss_pct = impact_analysis.estimated_production_loss_percent

        summary = (
            f"Supply chain disruption presents a {severity} operational risk across {plant_str}, "
            f"with an estimated overall production impact of {loss_pct:.1f}%. "
            f"The primary mitigation strategy focuses on aggressive inventory rebalancing, "
            f"engaging backup suppliers, and re-routing logistics corridors to secure raw material feeds."
        )
        return summary

    def _generate_executive_recommendation(self, impact_analysis: ImpactAnalysis) -> str:
        """Synthesize a concise executive directive."""
        severity = impact_analysis.overall_severity

        if severity == SeverityLevel.CRITICAL:
            return "Immediate executive intervention required: Authorize emergency procurement funds and activate alternate supplier contingency contracts."
        elif severity == SeverityLevel.HIGH:
            return "Approve rapid inventory rebalancing across primary facilities and shift transportation to priority freight corridors."
        elif severity == SeverityLevel.MEDIUM:
            return "Authorize procurement teams to negotiate backup supply allocations and adjust plant production schedules."
        
        return "Maintain active monitoring of supply buffers and enforce standard operational review protocols."

    def _estimate_recovery(self, impact_analysis: ImpactAnalysis) -> str:
        """Determine estimated operational recovery time based on severity level."""
        severity = impact_analysis.overall_severity

        if severity == SeverityLevel.CRITICAL:
            return "2–4 Weeks"
        elif severity == SeverityLevel.HIGH:
            return "1–2 Weeks"
        elif severity == SeverityLevel.MEDIUM:
            return "3–7 Days"

        return "1–3 Days"

    def _estimate_cost(self, impact_analysis: ImpactAnalysis) -> str:
        """Provide a qualitative human-readable cost estimate based on overall production loss."""
        loss_pct = impact_analysis.estimated_production_loss_percent

        if loss_pct >= COST_THRESHOLD_VERY_HIGH:
            return "Very High ($500k+ operational impact)"
        elif loss_pct >= COST_THRESHOLD_HIGH:
            return "High ($150k - $500k operational impact)"
        elif loss_pct >= COST_THRESHOLD_MEDIUM:
            return "Medium ($50k - $150k operational impact)"

        return "Low (<$50k operational impact)"

    def _build_result(
        self,
        alternate_suppliers: List[AlternateSupplier],
        transport_plan: List[TransportRecommendation],
        inventory_plan: List[InventoryRecommendation],
        production_plan: List[ProductionRecommendation],
        actions: List[MitigationAction],
        summary: str,
        executive_rec: str,
        recovery_est: str,
        cost_est: str,
        overall_priority: SeverityLevel,
    ) -> MitigationPlan:
        """Assemble the final MitigationPlan Pydantic instance."""
        return MitigationPlan(
            alternate_suppliers=alternate_suppliers,
            transportation_plan=transport_plan,
            inventory_plan=inventory_plan,
            production_plan=production_plan,
            actions=actions,
            summary=summary,
            executive_recommendation=executive_rec,
            recovery_estimate=recovery_est,
            estimated_cost=cost_est,
            overall_priority=overall_priority,
        )

    def _build_fallback_result(self, impact_analysis: ImpactAnalysis) -> MitigationPlan:
        """Provide a safe fallback MitigationPlan in case of unexpected processing exceptions."""
        return MitigationPlan(
            alternate_suppliers=[],
            transportation_plan=[
                TransportRecommendation(
                    mode="Road",
                    description="Standard transportation fallback route.",
                )
            ],
            inventory_plan=[],
            production_plan=[],
            actions=[
                MitigationAction(
                    title="Manual Review",
                    description="Perform manual supply chain review due to mitigation evaluation error.",
                    priority=SeverityLevel.HIGH,
                    estimated_duration="Immediate",
                )
            ],
            summary="Emergency fallback mitigation plan triggered.",
            executive_recommendation="Conduct manual operational assessment immediately.",
            recovery_estimate="Unknown",
            estimated_cost="Uncertain",
            overall_priority=impact_analysis.overall_severity if hasattr(impact_analysis, "overall_severity") else SeverityLevel.HIGH,
        )