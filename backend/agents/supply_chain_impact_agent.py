# backend/agents/supply_chain_impact_agent.py
"""
Supply Chain Impact Agent: The main business reasoning agent in the pipeline.

Inputs:
  - RiskAssessment (or RiskAnalysis)
  - KnowledgeGraphAgent
  - Inventory data
  - Plant data
  - Supplier data

Output:
  - ImpactAnalysis (structured Pydantic object)
"""

import json
import logging
from pathlib import Path
from typing import Any

from backend.agents.knowledge_graph_agent import KnowledgeGraphAgent, knowledge_graph_agent
from backend.models.enums import BusinessImpact, SeverityLevel
from backend.models.impact import ImpactAnalysis, InventoryImpactDetails, PlantImpactDetails
from backend.models.risk import RiskAnalysis, RiskAssessment
from backend.models.supply_chain import MatchedSupplier

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class SupplyChainImpactAgent:
    """
    Main business reasoning agent that calculates downstream impact,
    remaining operational inventory days, production loss (TPD), and total blast radius.
    """

    def __init__(
        self,
        kg_agent: KnowledgeGraphAgent | None = None,
        data_dir: Path = DATA_DIR,
    ):
        self.kg_agent = kg_agent or knowledge_graph_agent
        self.data_dir = data_dir
        self.inventory_data = self._load_json("inventory/inventory.json").get("plant_inventories", [])
        self.plants_data = self._load_json("plants/plants.json").get("plants", [])
        self.suppliers_data = self._load_json("suppliers/suppliers.json").get("suppliers", [])
        self.warehouses_data = self._load_json("warehouses/warehouses.json").get("warehouses", [])
        self.distribution_data = self._load_json("distribution/distribution_centers.json").get(
            "distribution_centers", []
        )

    def _load_json(self, relative_path: str) -> dict:
        """Loads a JSON file relative to the data directory."""
        full_path = self.data_dir / relative_path
        if not full_path.exists():
            logger.warning("Data file not found: %s", full_path)
            return {}
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("Error loading JSON file %s: %s", full_path, exc)
            return {}

    def analyze_impact(
        self,
        assessment_input: RiskAssessment | RiskAnalysis,
        matched_suppliers: list[MatchedSupplier] | None = None,
    ) -> ImpactAnalysis:
        """
        Calculates the complete downstream impact analysis from a disruption assessment.
        """
        # Unpack assessment if passed as RiskAnalysis
        if isinstance(assessment_input, RiskAnalysis):
            assessment = assessment_input.assessment
            if matched_suppliers is None:
                matched_suppliers = assessment_input.matched_suppliers
        else:
            assessment = assessment_input

        matched_suppliers = matched_suppliers or []

        # 1. Gather initial affected suppliers
        initial_supplier_ids: set[str] = set()
        matched_supplier_objects: list[MatchedSupplier] = []

        for ms in matched_suppliers:
            initial_supplier_ids.add(ms.supplier_id)
            matched_supplier_objects.append(ms)

        # Match text-based affected suppliers from assessment against database
        for aff_entity in getattr(assessment, "affected_suppliers", []):
            entity_name = aff_entity.name if hasattr(aff_entity, "name") else str(aff_entity)
            for sup in self.suppliers_data:
                if (
                    sup["supplier_id"].lower() == entity_name.lower()
                    or sup["supplier_name"].lower() in entity_name.lower()
                    or entity_name.lower() in sup["supplier_name"].lower()
                ):
                    initial_supplier_ids.add(sup["supplier_id"])

        # Also check affected materials from assessment
        initial_material_ids: set[str] = set()
        for mat in getattr(assessment, "affected_materials", []):
            mat_str = str(mat).upper()
            # If mat_str matches a known material_id or name
            for inv in self.inventory_data:
                if inv.get("material_id") == mat_str or inv.get("material_name", "").lower() in mat_str.lower():
                    initial_material_ids.add(inv["material_id"])

        # 2. Graph Traversal for blast radius
        affected_suppliers: set[str] = set(initial_supplier_ids)
        affected_materials: set[str] = set(initial_material_ids)
        affected_plants: set[str] = set()
        affected_warehouses: set[str] = set()
        affected_dcs: set[str] = set()

        for sup_id in initial_supplier_ids:
            downstream = self.kg_agent.get_downstream_impact(sup_id)
            affected_materials.update(downstream.get("material", []))
            affected_plants.update(downstream.get("plant", []))
            affected_warehouses.update(downstream.get("warehouse", []))
            affected_dcs.update(downstream.get("distribution_center", []))

            # Direct supplier-to-plant edges
            for plant_info in self.kg_agent.get_plants_supplied_by(sup_id):
                affected_plants.add(plant_info["plant_id"])

        for mat_id in initial_material_ids:
            # Add materials to affected materials
            affected_materials.add(mat_id)
            # Find plants consuming this material from inventory data
            for inv in self.inventory_data:
                if inv.get("material_id") == mat_id:
                    affected_plants.add(inv["plant_id"])

        # For affected plants, gather connected warehouses and distribution centers
        for plant_id in list(affected_plants):
            dcs = self.kg_agent.get_distribution_centers_for_plant(plant_id)
            affected_dcs.update(dcs)
            # Find warehouses supplying this plant
            for wh in self.warehouses_data:
                # If warehouse plant mapping or plant warehouse ID matches
                for plant_item in self.plants_data:
                    if plant_item.get("plant_id") == plant_id:
                        if plant_item.get("warehouse_id"):
                            affected_warehouses.add(plant_item["warehouse_id"])
                        if plant_item.get("distribution_center_id"):
                            affected_dcs.add(plant_item["distribution_center_id"])

        # Ensure matched suppliers from database are included in affected_suppliers list
        affected_suppliers_output: list[MatchedSupplier | str] = []
        seen_sup_ids = set()
        for ms in matched_supplier_objects:
            affected_suppliers_output.append(ms)
            seen_sup_ids.add(ms.supplier_id)

        for sup_id in sorted(affected_suppliers):
            if sup_id not in seen_sup_ids:
                # Look up supplier details from data
                sup_record = next((s for s in self.suppliers_data if s["supplier_id"] == sup_id), None)
                if sup_record:
                    affected_suppliers_output.append(
                        MatchedSupplier(
                            supplier_id=sup_record["supplier_id"],
                            supplier_name=sup_record["supplier_name"],
                            city=sup_record.get("city"),
                            state=sup_record.get("state"),
                            country=sup_record.get("country"),
                            materials=sup_record.get("materials", []),
                            reliability_score=sup_record.get("reliability_score"),
                            business_priority=sup_record.get("business_priority"),
                            match_reason="graph_traversal",
                        )
                    )
                else:
                    affected_suppliers_output.append(sup_id)

        # 3. Inventory Impact Calculation
        inventory_details: list[InventoryImpactDetails] = []
        remaining_days_list: list[float] = []

        for inv in self.inventory_data:
            p_id = inv.get("plant_id")
            m_id = inv.get("material_id")
            s_id = inv.get("supplier_id")

            # Check if this inventory is at risk
            is_affected = (
                (p_id in affected_plants)
                or (m_id in affected_materials)
                or (s_id in affected_suppliers)
            )

            if is_affected:
                rem_days = float(inv.get("remaining_operational_days", 0.0))
                remaining_days_list.append(rem_days)
                inventory_details.append(
                    InventoryImpactDetails(
                        inventory_id=inv["inventory_id"],
                        plant_id=p_id,
                        material_id=m_id,
                        material_name=inv.get("material_name", m_id),
                        supplier_id=s_id,
                        available_stock_tons=float(inv.get("available_stock_tons", 0.0)),
                        daily_consumption_tons=float(inv.get("daily_consumption_tons", 0.0)),
                        remaining_operational_days=rem_days,
                        inventory_status=inv.get("inventory_status", "Warning"),
                        criticality=inv.get("criticality", "MEDIUM"),
                    )
                )

        est_remaining_days = min(remaining_days_list) if remaining_days_list else 30.0

        if est_remaining_days < 7.0:
            overall_inv_status = "CRITICAL: Stockout expected within 7 days"
        elif est_remaining_days < 14.0:
            overall_inv_status = "HIGH RISK: Stockout expected within 14 days"
        elif est_remaining_days < 30.0:
            overall_inv_status = "MODERATE RISK: Inventory buffer active (14-30 days remaining)"
        else:
            overall_inv_status = "HEALTHY: Adequate inventory stock available (>30 days)"

        # 4. Production Impact Calculation
        plant_details: list[PlantImpactDetails] = []
        total_production_loss_tpd = 0.0
        total_capacity_tpd = 0.0

        for p_item in self.plants_data:
            p_id = p_item["plant_id"]
            cap_tpd = float(p_item.get("production_capacity_tpd", 0.0))
            curr_tpd = float(p_item.get("current_daily_production_tpd", cap_tpd))
            total_capacity_tpd += cap_tpd

            if p_id in affected_plants:
                # Calculate estimated loss based on severity of disruption or remaining days
                if est_remaining_days < 7.0:
                    loss_tpd = curr_tpd  # 100% loss imminent
                elif est_remaining_days < 14.0:
                    loss_tpd = curr_tpd * 0.5  # 50% partial reduction
                else:
                    loss_tpd = curr_tpd * 0.2  # 20% potential constraint

                total_production_loss_tpd += loss_tpd
                plant_details.append(
                    PlantImpactDetails(
                        plant_id=p_id,
                        plant_name=p_item.get("plant_name", p_id),
                        city=p_item.get("city"),
                        state=p_item.get("state"),
                        production_capacity_tpd=cap_tpd,
                        current_daily_production_tpd=curr_tpd,
                        estimated_production_loss_tpd=loss_tpd,
                        operating_status=p_item.get("operating_status", "OPERATIONAL"),
                    )
                )

        if total_production_loss_tpd > 0:
            pct_loss = (total_production_loss_tpd / total_capacity_tpd * 100) if total_capacity_tpd > 0 else 0.0
            prod_impact_str = (
                f"Estimated production loss of {total_production_loss_tpd:,.0f} TPD "
                f"({pct_loss:.1f}% of total enterprise capacity) across {len(plant_details)} plant(s)."
            )
        else:
            prod_impact_str = "No immediate daily production capacity loss projected."

        # 5. Blast Radius Description
        blast_radius_count = (
            len(affected_suppliers)
            + len(affected_materials)
            + len(affected_plants)
            + len(affected_warehouses)
            + len(affected_dcs)
        )

        blast_radius_str = (
            f"Supply Chain Blast Radius: {blast_radius_count} network nodes affected "
            f"({len(affected_suppliers)} supplier(s), {len(affected_materials)} material(s), "
            f"{len(affected_plants)} plant(s), {len(affected_warehouses)} warehouse(s), "
            f"{len(affected_dcs)} distribution center(s))."
        )

        # 6. Severity & Business Impact Assessment
        severity = assessment.severity
        business_impact = assessment.business_impact

        # Escalate severity if remaining operational days are critical (< 7 days)
        if est_remaining_days < 7.0 and severity in (SeverityLevel.LOW, SeverityLevel.MEDIUM):
            severity = SeverityLevel.HIGH
        if total_production_loss_tpd > 10000 and business_impact in (BusinessImpact.LOW, BusinessImpact.MEDIUM):
            business_impact = BusinessImpact.HIGH

        # 7. Confidence Score
        confidence = float(getattr(assessment, "confidence", 0.85))
        if matched_supplier_objects:
            confidence = min(1.0, confidence + 0.05)

        return ImpactAnalysis(
            affected_suppliers=affected_suppliers_output,
            affected_materials=sorted(list(affected_materials)),
            affected_plants=sorted(list(affected_plants)),
            affected_warehouses=sorted(list(affected_warehouses)),
            affected_distribution_centers=sorted(list(affected_dcs)),
            inventory_status=overall_inv_status,
            estimated_inventory_remaining_days=round(est_remaining_days, 2),
            production_impact=prod_impact_str,
            business_impact=business_impact,
            supply_chain_blast_radius=blast_radius_str,
            overall_impact_severity=severity,
            confidence_score=round(confidence, 2),
            inventory_details=inventory_details,
            plant_details=plant_details,
        )

