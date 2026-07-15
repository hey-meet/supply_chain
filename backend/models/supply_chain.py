# backend/models/supply_chain.py
"""
This file defines what ONE "matched supplier" result looks like.

"""

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import MatchReason


class MatchedSupplier(BaseModel):
    """
    One real supplier from our database, confirmed to be relevant to a
    disruption (either because the article named them, or because
    they're located in the affected area, or both).
    """

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    # Basic identifying info, copied straight from our supplier database.
    supplier_id: str = Field(..., description="Our internal supplier ID, e.g. 'SUP-001'.")
    supplier_name: str = Field(..., description="The supplier's registered name.")

    # Where the supplier is based. 
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)

    # What this supplier provides us
    materials: list[str] = Field(
        default_factory=list,
        description="Material IDs this supplier provides (e.g. 'MAT-LMS-01').",
    )
    reliability_score: float | None = Field(default=None)
    business_priority: str | None = Field(default=None)

    # WHY we matched this supplier to the disruption. One of:
    #   "name"              -> the article mentioned this supplier by name
    #   "location"           -> this supplier is based in the affected area
    #   "name_and_location"  -> both of the above are true
    match_reason: MatchReason = Field(
        ...,
        description=(
            "Why this supplier was flagged: 'name', 'location', "
            "or 'name_and_location'."
        ),
    )
