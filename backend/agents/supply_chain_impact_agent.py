"""
Supply Chain Impact Agent module for Cement Manufacturing Autonomous Monitoring.

This module evaluates operational and supply chain impacts triggered by external risks
and supplier disruptions. It strictly consumes existing domain models from the project's
central models package and uses deterministic business logic, local dataset indexes,
and Knowledge Graph contextual queries to determine overall production losses and risks.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Project Models & Enums
from backend.models.enums import BusinessImpact, SeverityLevel
from backend.models.impact import ImpactAnalysis, InventoryImpact, PlantImpact
from backend.models.risk import RiskAnalysis
from backend.agents.knowledge_graph_agent import knowledge_graph_agent
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURABLE CONSTANTS & THRESHOLDS
# ============================================================================

DEFAULT_DATA_DIR = Path("backend/data")

# Inventory operational days thresholds for production loss risk tiers
THRESHOLD_DAYS_VERY_HIGH = 2.0
THRESHOLD_DAYS_HIGH = 5.0
THRESHOLD_DAYS_MEDIUM = 10.0

# Base production loss percentages by risk tier
LOSS_PCT_VERY_HIGH = 85.0
LOSS_PCT_HIGH = 50.0
LOSS_PCT_MEDIUM = 20.0
LOSS_PCT_LOW = 5.0

# Criticality weighting multipliers
CRITICALITY_MULTIPLIERS: Dict[str, float] = {
    "CRITICAL": 1.5,
    "HIGH": 1.25,
    "MEDIUM": 1.0,
    "LOW": 0.75,
}

DEFAULT_CRITICALITY_MULTIPLIER = 1.0


# ============================================================================
# SUPPLY CHAIN IMPACT AGENT
# ============================================================================

class SupplyChainImpactAgent:
    """
    Computes operational and supply chain impacts for cement manufacturing.
    
    Evaluates plant operational degradation, inventory exhaustion timelines,
    and mitigation routes strictly via deterministic rules and local datasets.
    """

    def __init__(
        self,
        knowledge_graph_agent: Any,
        data_dir: Path = DEFAULT_DATA_DIR
    ) -> None:
        """
        Initialize the SupplyChainImpactAgent and index lookup datasets.

        :param knowledge_graph_agent: Implemented Knowledge Graph Agent instance.
        :param data_dir: Directory path containing domain JSON files.
        """
        self.kg_agent = knowledge_graph_agent
        self.data_dir = Path(data_dir)

        # Datasets loaded from JSON
        self.plants_data: List[Dict[str, Any]] = []
        self.inventory_data: List[Dict[str, Any]] = []
        self.suppliers_data: List[Dict[str, Any]] = []
        self.warehouses_data: List[Dict[str, Any]] = []
        self.plant_supplier_map: List[Dict[str, Any]] = []
        self.material_supplier_map: List[Dict[str, Any]] = []

        # Fast lookup indexes initialized during startup
        self._plant_by_id: Dict[str, Dict[str, Any]] = {}
        self._supplier_by_id: Dict[str, Dict[str, Any]] = {}
        self._inventory_by_supplier: Dict[str, List[Dict[str, Any]]] = {}
        self._inventory_by_plant: Dict[str, List[Dict[str, Any]]] = {}
        self._warehouse_by_id: Dict[str, Dict[str, Any]] = {}
        self._material_map_by_id: Dict[str, Dict[str, Any]] = {}

        self._load_datasets()

    def _load_json(self, file_name: str, primary_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Safely load and parse a JSON dataset file handling top-level object wrappers.

        :param file_name: JSON file name under data_dir.
        :param primary_key: Optional expected key for wrapped lists (e.g., 'plants', 'inventory').
        """
        file_path = self.data_dir / file_name
        if not file_path.is_file():
            logger.warning(f"Dataset file not found: {file_path}. Defaulting to empty collection.")
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    if primary_key and primary_key in data and isinstance(data[primary_key], list):
                        return data[primary_key]
                    # Fallback scan for any embedded list
                    for value in data.values():
                        if isinstance(value, list):
                            return value
                    return [data]
                return []
        except Exception as err:
            logger.error(f"Failed to parse JSON file {file_path}: {err}")
            return []

    def _load_datasets(self) -> None:
        """Load JSON datasets into memory and build high-performance indexing dictionaries."""
        self.plants_data = self._load_json("plants/plants.json", primary_key="plants")
        self.inventory_data = self._load_json("inventory/inventory.json", primary_key="inventory")
        self.suppliers_data = self._load_json("suppliers/suppliers.json", primary_key="suppliers")
        self.warehouses_data = self._load_json("warehouses/warehouses.json", primary_key="warehouses")
        self.plant_supplier_map = self._load_json("relationships/plant_supplier_map.json", primary_key="plant_supplier_mappings")
        self.material_supplier_map = self._load_json("relationships/material_supplier_map.json", primary_key="material_supplier_mappings")

        # Index Plants
        for p in self.plants_data:
            p_id = p.get("plant_id")
            if p_id:
                self._plant_by_id[p_id] = p

        # Index Suppliers
        for s in self.suppliers_data:
            s_id = s.get("supplier_id")
            if s_id:
                self._supplier_by_id[s_id] = s

        # Index Inventory by Supplier and Plant
        for inv in self.inventory_data:
            s_id = inv.get("supplier_id")
            p_id = inv.get("plant_id")
            if s_id:
                self._inventory_by_supplier.setdefault(s_id, []).append(inv)
            if p_id:
                self._inventory_by_plant.setdefault(p_id, []).append(inv)

        # Index Warehouses
        for w in self.warehouses_data:
            w_id = w.get("warehouse_id")
            if w_id:
                self._warehouse_by_id[w_id] = w

        # Index Material Map
        for m in self.material_supplier_map:
            m_id = m.get("material_id")
            if m_id:
                self._material_map_by_id[m_id] = m

        logger.info("Successfully loaded and indexed all supply chain datasets.")

    def analyze(self, risk_analysis: RiskAnalysis) -> ImpactAnalysis:
        """
        Main entrypoint: Performs deterministic business reasoning over input risk context.

        :param risk_analysis: Validated output from Risk Classification Agent.
        :return: Fully constructed ImpactAnalysis Pydantic model instance.
        """
        logger.info("Analyzing supply chain impact for risk assessment.")

        disrupted_suppliers = risk_analysis.matched_suppliers
        disrupted_supplier_ids = {s.supplier_id for s in disrupted_suppliers if s.supplier_id}

        # Step 1: Collect Context from KnowledgeGraphAgent
        graph_context = self._collect_graph_context(disrupted_supplier_ids)

        # Step 2: Analyze Inventory Impact
        affected_inventories = self._analyze_inventory(disrupted_supplier_ids)

        # Step 3: Analyze Plant Operational Impact
        affected_plants, total_loss_pct = self._analyze_plants(
            disrupted_supplier_ids,
            graph_context["plant_ids"],
            graph_context["material_ids"],
            affected_inventories
        )

        # Step 4: Extract Warehouses and Distribution Centers
        affected_warehouses = self._collect_affected_warehouses(
            affected_plants, affected_inventories
        )
        affected_dcs = list(graph_context["dc_ids"])

        # Step 5: Resolve Alternate Suppliers
        alternates = self._resolve_alternate_suppliers(
            disrupted_supplier_ids, graph_context["alternates"]
        )

        # Step 6: Compute Derived Business Metrics
        business_impact = self._calculate_business_impact(
            affected_plants, affected_inventories, total_loss_pct
        )
        overall_severity = self._calculate_overall_severity(
            affected_plants, affected_inventories, total_loss_pct
        )

        # Step 7: Build Human-Readable Explanation
        reasoning = self._build_reasoning(
            risk_analysis,
            affected_plants,
            affected_inventories,
            overall_severity,
            business_impact
        )

        return self._build_result(
            risk=risk_analysis,
            plants=affected_plants,
            warehouses=affected_warehouses,
            dcs=affected_dcs,
            inventories=affected_inventories,
            alternates=alternates,
            dependency_chain=graph_context["dependency_chain"],
            business_impact=business_impact,
            severity=overall_severity,
            loss_pct=total_loss_pct,
            reasoning=reasoning
        )

    def _collect_graph_context(self, supplier_ids: Set[str]) -> Dict[str, Any]:
        """Query KnowledgeGraphAgent public APIs for interconnected entity impact."""
        affected_plants: Set[str] = set()
        affected_materials: Set[str] = set()
        affected_dcs: Set[str] = set()
        alternates: List[str] = []
        dependency_chain: List[Dict[str, Any]] = []

        for sup_id in supplier_ids:
            try:
                plants = self.kg_agent.get_affected_plants(sup_id) or []
                affected_plants.update(plants)
            except Exception as err:
                logger.warning(f"Error querying KG plants for supplier {sup_id}: {err}")

            try:
                materials = self.kg_agent.get_affected_materials(sup_id) or []
                affected_materials.update(materials)
            except Exception as err:
                logger.warning(f"Error querying KG materials for supplier {sup_id}: {err}")

            try:
                dcs = self.kg_agent.get_affected_distribution_centers(sup_id) or []
                affected_dcs.update(dcs)
            except Exception as err:
                logger.warning(f"Error querying KG DCs for supplier {sup_id}: {err}")

            try:
                alts = self.kg_agent.get_alternate_suppliers(sup_id) or []
                if isinstance(alts, list):
                    alternates.extend(alts)
            except Exception as err:
                logger.warning(f"Error querying KG alternates for supplier {sup_id}: {err}")

            try:
                chain = self.kg_agent.get_dependency_chain(sup_id) or []
                if isinstance(chain, list):
                    dependency_chain.extend(chain)
            except Exception as err:
                logger.warning(f"Error querying KG dependency chain for supplier {sup_id}: {err}")

        return {
            "plant_ids": affected_plants,
            "material_ids": affected_materials,
            "dc_ids": affected_dcs,
            "alternates": alternates,
            "dependency_chain": dependency_chain
        }

    def _analyze_inventory(self, disrupted_supplier_ids: Set[str]) -> List[InventoryImpact]:
        """Scan inventory items linked to disrupted suppliers and construct InventoryImpact Pydantic models."""
        results: List[InventoryImpact] = []
        seen_keys: Set[Tuple[str, str, str]] = set()

        for sup_id in disrupted_supplier_ids:
            items = self._inventory_by_supplier.get(sup_id, [])
            for item in items:
                p_id = item.get("plant_id", "")
                m_id = item.get("material_id", "")
                key = (p_id, sup_id, m_id)

                if key in seen_keys:
                    continue
                seen_keys.add(key)

                rem_days = float(item.get("remaining_operational_days", 999.0))

                results.append(
                    InventoryImpact(
                        plant_id=p_id,
                        material=item.get("material_name", m_id),
                        current_stock_days=rem_days,
                        status=item.get("inventory_status", "UNKNOWN")
                    )
                )

        return results

    def _analyze_plants(
        self,
        disrupted_supplier_ids: Set[str],
        kg_plant_ids: Set[str],
        kg_material_ids: Set[str],
        affected_inventories: List[InventoryImpact]
    ) -> Tuple[List[PlantImpact], float]:
        """Calculate production loss per plant and construct PlantImpact Pydantic models."""
        combined_plant_ids = set(kg_plant_ids)
        for inv in affected_inventories:
            if inv.plant_id:
                combined_plant_ids.add(inv.plant_id)

        # Cross-reference with plant_supplier_map
        for p_map in self.plant_supplier_map:
            p_id = p_map.get("plant_id")
            primaries = p_map.get("primary_suppliers", [])
            secondaries = p_map.get("secondary_suppliers", [])
            all_sups = set(primaries + secondaries)
            if p_id and not all_sups.isdisjoint(disrupted_supplier_ids):
                combined_plant_ids.add(p_id)

        # Build fast lookup dictionary grouping affected inventories by plant_id O(1)
        invs_by_plant: Dict[str, List[InventoryImpact]] = {}
        for inv in affected_inventories:
            if inv.plant_id:
                invs_by_plant.setdefault(inv.plant_id, []).append(inv)

        plant_impacts: List[PlantImpact] = []
        total_capacity = 0.0
        total_loss_tpd = 0.0

        for p_id in sorted(combined_plant_ids):
            plant_info = self._plant_by_id.get(p_id)
            if not plant_info:
                continue

            capacity = float(plant_info.get("production_capacity_tpd", 0.0))
            current_prod = float(plant_info.get("current_daily_production_tpd", capacity))

            # Retrieve pre-grouped inventory items for this plant in O(1)
            plant_invs = invs_by_plant.get(p_id, [])
            affected_materials = list({inv.material for inv in plant_invs if inv.material}.union(kg_material_ids))

            # Extract affected suppliers for this plant
            p_inv_raw = self._inventory_by_plant.get(p_id, [])
            affected_sups = list({item.get("supplier_id") for item in p_inv_raw if item.get("supplier_id") in disrupted_supplier_ids})

            loss_pct = self._calculate_production_loss(plant_invs)
            loss_tpd = current_prod * (loss_pct / 100.0)

            total_capacity += current_prod
            total_loss_tpd += loss_tpd

            plant_impacts.append(
                PlantImpact(
                    plant_id=p_id,
                    plant_name=plant_info.get("plant_name", p_id),
                    affected_materials=affected_materials,
                    affected_suppliers=affected_sups,
                    production_loss_percent=round(loss_pct, 2)
                )
            )

        aggregate_loss_pct = 0.0
        if total_capacity > 0:
            aggregate_loss_pct = round((total_loss_tpd / total_capacity) * 100.0, 2)

        return plant_impacts, aggregate_loss_pct

    def _calculate_production_loss(self, plant_inventories: List[InventoryImpact]) -> float:
        """Estimate production loss percentage for a plant based on critical inventory depletion."""
        if not plant_inventories:
            return LOSS_PCT_LOW

        max_loss = 0.0
        for inv in plant_inventories:
            days = inv.current_stock_days

            if days < THRESHOLD_DAYS_VERY_HIGH:
                base_loss = LOSS_PCT_VERY_HIGH
            elif days < THRESHOLD_DAYS_HIGH:
                base_loss = LOSS_PCT_HIGH
            elif days < THRESHOLD_DAYS_MEDIUM:
                base_loss = LOSS_PCT_MEDIUM
            else:
                base_loss = LOSS_PCT_LOW

            # Lookup material criticality from the indexed raw inventory dataset (Option B)
            raw_items = self._inventory_by_plant.get(inv.plant_id, [])
            criticality_str = "MEDIUM"
            for r_item in raw_items:
                if r_item.get("material_name") == inv.material or r_item.get("material_id") == inv.material:
                    criticality_str = str(r_item.get("criticality", "MEDIUM")).upper()
                    break

            mult = CRITICALITY_MULTIPLIERS.get(criticality_str, DEFAULT_CRITICALITY_MULTIPLIER)
            adjusted_loss = min(100.0, base_loss * mult)

            if adjusted_loss > max_loss:
                max_loss = adjusted_loss

        return max_loss

    def _calculate_business_impact(
        self,
        affected_plants: List[PlantImpact],
        affected_inventories: List[InventoryImpact],
        total_loss_pct: float
    ) -> BusinessImpact:
        """Compute the overall business impact rating."""
        num_plants = len(affected_plants)
        min_days = min((inv.current_stock_days for inv in affected_inventories), default=999.0)

        if total_loss_pct >= 60.0 or (num_plants >= 3 and min_days < THRESHOLD_DAYS_VERY_HIGH):
            return BusinessImpact.SEVERE
        elif total_loss_pct >= 35.0 or min_days < THRESHOLD_DAYS_HIGH:
            return BusinessImpact.HIGH
        elif total_loss_pct >= 15.0 or min_days < THRESHOLD_DAYS_MEDIUM:
            return BusinessImpact.MEDIUM
        elif total_loss_pct > 0.0:
            return BusinessImpact.LOW

        return BusinessImpact.LOW

    def _calculate_overall_severity(
        self,
        affected_plants: List[PlantImpact],
        affected_inventories: List[InventoryImpact],
        total_loss_pct: float
    ) -> SeverityLevel:
        """Compute the operational severity level."""
        min_days = min((inv.current_stock_days for inv in affected_inventories), default=999.0)
        num_plants = len(affected_plants)

        if min_days < THRESHOLD_DAYS_VERY_HIGH or total_loss_pct >= 50.0:
            return SeverityLevel.CRITICAL
        elif min_days < THRESHOLD_DAYS_HIGH or total_loss_pct >= 30.0 or num_plants >= 2:
            return SeverityLevel.HIGH
        elif min_days < THRESHOLD_DAYS_MEDIUM or total_loss_pct >= 10.0:
            return SeverityLevel.MEDIUM

        return SeverityLevel.LOW

    def _collect_affected_warehouses(
        self,
        plants: List[PlantImpact],
        inventories: List[InventoryImpact]
    ) -> List[str]:
        """Aggregate unique warehouse IDs connected to affected plants and inventories."""
        warehouses: Set[str] = set()

        for inv in inventories:
            p_inv_items = self._inventory_by_plant.get(inv.plant_id, [])
            for item in p_inv_items:
                w_id = item.get("warehouse_id")
                if w_id:
                    warehouses.add(w_id)

        for p in plants:
            p_info = self._plant_by_id.get(p.plant_id, {})
            w_id = p_info.get("warehouse_id")
            if w_id:
                warehouses.add(w_id)

        return sorted(warehouses)

    def _resolve_alternate_suppliers(
        self,
        disrupted_supplier_ids: Set[str],
        kg_alternates: List[Any]
    ) -> List[str]:
        """Deduplicate and format alternate supplier identifiers as strings."""
        alternates_set: Set[str] = set()

        # Add KG alternates (handling string IDs/names or dict returns)
        for alt in kg_alternates:
            if isinstance(alt, str):
                s_info = self._supplier_by_id.get(alt, {})
                alternates_set.add(s_info.get("supplier_name", alt))
            elif isinstance(alt, dict):
                s_id = alt.get("supplier_id") or alt.get("id", "")
                s_info = self._supplier_by_id.get(s_id, {})
                supplier_name = s_info.get("supplier_name", alt.get("supplier_name", s_id))
                if supplier_name:
                    alternates_set.add(supplier_name)

        # Lookup backup suppliers in material_supplier_map
        for m_map in self.material_supplier_map:
            prim_sup = m_map.get("primary_supplier", "")
            if prim_sup in disrupted_supplier_ids:
                backups = m_map.get("backup_suppliers", [])
                for b_id in backups:
                    if b_id not in disrupted_supplier_ids:
                        b_info = self._supplier_by_id.get(b_id, {})
                        alternates_set.add(b_info.get("supplier_name", b_id))

        return sorted(alternates_set)

    def _build_reasoning(
        self,
        risk_analysis: RiskAnalysis,
        plants: List[PlantImpact],
        inventories: List[InventoryImpact],
        severity: SeverityLevel,
        impact: BusinessImpact
    ) -> str:
        """Synthesize a human-readable summary of operational disruption reasoning."""
        matched_sups = risk_analysis.matched_suppliers
        sup_names = ", ".join([s.supplier_name for s in matched_sups]) or "Unknown Suppliers"

        all_materials = set()
        for s in matched_sups:
            all_materials.update(s.materials)
        mat_str = ", ".join(sorted(all_materials)) or "critical materials"

        num_plants = len(plants)
        plant_str = f"{num_plants} manufacturing plant{'s' if num_plants != 1 else ''}"

        critical_invs = [inv for inv in inventories if inv.current_stock_days <= THRESHOLD_DAYS_HIGH]

        if critical_invs:
            min_inv = min(critical_invs, key=lambda x: x.current_stock_days)
            inv_clause = (
                f"Inventory analysis reveals critical stock depletion at {min_inv.plant_id} "
                f"with only {min_inv.current_stock_days:.1f} operational days remaining "
                f"for {min_inv.material}."
            )
        else:
            inv_clause = "Current inventory levels provide adequate buffer across all operational plants."

        reasoning = (
            f"The disruption affects primary supplier(s) ({sup_names}) providing {mat_str} "
            f"to {plant_str}. {inv_clause} "
            f"This raises the overall operational severity to {severity.value} "
            f"and business impact to {impact.value}."
        )

        return reasoning

    def _build_result(
        self,
        risk: RiskAnalysis,
        plants: List[PlantImpact],
        warehouses: List[str],
        dcs: List[str],
        inventories: List[InventoryImpact],
        alternates: List[str],
        dependency_chain: List[Dict[str, Any]],
        business_impact: BusinessImpact,
        severity: SeverityLevel,
        loss_pct: float,
        reasoning: str
    ) -> ImpactAnalysis:
        """Construct the final ImpactAnalysis Pydantic model instance."""
        return ImpactAnalysis(
            risk=risk,
            affected_plants=plants,
            affected_warehouses=warehouses,
            affected_distribution_centers=dcs,
            inventory=inventories,
            alternate_suppliers=alternates,
            dependency_chain=dependency_chain,
            overall_business_impact=business_impact,
            overall_severity=severity,
            estimated_production_loss_percent=loss_pct,
            reasoning=reasoning
        )


# Exported agent instance
supply_chain_impact_agent = SupplyChainImpactAgent(
    knowledge_graph_agent=knowledge_graph_agent
)