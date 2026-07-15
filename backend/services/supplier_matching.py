# backend/services/supplier_matching.py
"""
This file matches suppliers by name or by location or by both

"""

import json
import logging
from pathlib import Path
 
from backend.models.location import Location
from backend.models.risk import RiskAssessment
from backend.models.supply_chain import MatchedSupplier
 
logger = logging.getLogger(__name__)
 
# Where our real supplier data lives on disk.
# (this file is at backend/services/supplier_matching.py, so we go up
# one folder to backend/, then into data/suppliers/suppliers.json)
SUPPLIERS_DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "suppliers" / "suppliers.json"
)
 
 
def load_suppliers(path: Path = SUPPLIERS_DATA_PATH) -> list[dict]:
    """
    Reads our supplier database from disk and returns it as a list of dicts.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    return data.get("suppliers", [])
 
 
# -----------------------------------------------------------------------
# STEP 1: Match by NAME
# -----------------------------------------------------------------------
def match_by_name(entity_names: list[str], suppliers: list[dict]) -> list[str]:
    """
    Matches suppliers by name.
    Args:
        entity_names (list[str]): Names the AI extracted from the article.
        suppliers (list[dict]): Our full supplier database.
 
    Returns:
        list[str]: supplier_id values that matched by name (no duplicates).
    """
    matched_supplier_ids: list[str] = []
 
    for entity_name in entity_names:
        if not entity_name or not entity_name.strip():
            continue
 
        entity_name_lower = entity_name.strip().lower()
 
        for supplier in suppliers:
            supplier_name_lower = supplier.get("supplier_name", "").lower()
            if not supplier_name_lower:
                continue
 
            names_overlap = (
                entity_name_lower in supplier_name_lower
                or supplier_name_lower in entity_name_lower
            )
 
            if names_overlap:
                supplier_id = supplier["supplier_id"]
                if supplier_id not in matched_supplier_ids:
                    matched_supplier_ids.append(supplier_id)
 
    return matched_supplier_ids
 
 
# -----------------------------------------------------------------------
# STEP 2: Match by LOCATION
# -----------------------------------------------------------------------
def match_by_location(location: Location | None, suppliers: list[dict]) -> list[str]:
    """
    Match suppliers by location (state or city).
    Args:
        location (Location | None): Where the disruption is happening.
            If None (unknown location), there's nothing to compare
            against, so no matches are possible.
        suppliers (list[dict]): Our full supplier database.
 
    Returns:
        list[str]: supplier_id values that matched by location (no duplicates).
    """
    if location is None:
        return []
 
    location_state = (location.state or "").strip().lower()
    location_city = (location.city or "").strip().lower()
 
    matched_supplier_ids: list[str] = []
 
    for supplier in suppliers:
        supplier_state = (supplier.get("state") or "").strip().lower()
        supplier_city = (supplier.get("city") or "").strip().lower()
 
        same_state = location_state != "" and location_state == supplier_state
        same_city = location_city != "" and location_city == supplier_city
 
        if same_state or same_city:
            supplier_id = supplier["supplier_id"]
            if supplier_id not in matched_supplier_ids:
                matched_supplier_ids.append(supplier_id)
 
    return matched_supplier_ids
 
 
# -----------------------------------------------------------------------
# STEP 3: Combine both checks into the final result
# -----------------------------------------------------------------------
def find_known_suppliers(assessment: RiskAssessment) -> list[MatchedSupplier]:
    """
    Find known suppliers that match the given risk assessment based on name and location.
    Args:
        assessment (RiskAssessment): The AI's risk assessment for one article.
 
    Returns:
        list[MatchedSupplier]: Real suppliers connected to this
        disruption. Empty list if none matched, or if the supplier data
        couldn't be read.
    """
    try:
        suppliers = load_suppliers()
    except Exception as exc:
        logger.warning("Could not load supplier database — skipping supplier matching: %s", exc)
        return []
 
    # Gather the names the AI already guessed from the article text.
    entity_names = [entity.name for entity in assessment.affected_suppliers]
 
    name_matches = match_by_name(entity_names, suppliers)
    location_matches = match_by_location(assessment.location, suppliers)
 
    # Build the final list, one MatchedSupplier per unique supplier_id,
    # noting whether it matched by name, location, or both.
    matched_suppliers: list[MatchedSupplier] = []
 
    for supplier in suppliers:
        supplier_id = supplier["supplier_id"]
 
        matched_by_name = supplier_id in name_matches
        matched_by_location = supplier_id in location_matches
 
        if not matched_by_name and not matched_by_location:
            continue  # This supplier wasn't matched at all — skip it.
 
        if matched_by_name and matched_by_location:
            reason = "name_and_location"
        elif matched_by_name:
            reason = "name"
        else:
            reason = "location"
 
        matched_suppliers.append(
            MatchedSupplier(
                supplier_id=supplier_id,
                supplier_name=supplier["supplier_name"],
                city=supplier.get("city"),
                state=supplier.get("state"),
                country=supplier.get("country"),
                materials=supplier.get("materials", []),
                reliability_score=supplier.get("reliability_score"),
                business_priority=supplier.get("business_priority"),
                match_reason=reason,
            )
        )
 
    return matched_suppliers
