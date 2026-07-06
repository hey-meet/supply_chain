# backend/api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DisruptionDetail(BaseModel):
    category: str = Field(..., description="Risk category (e.g., Port Delay, Weather, Strike)")
    severity: str = Field(..., description="Severity level: LOW, MEDIUM, HIGH, CRITICAL")
    impact_score: float = Field(..., ge=0.0, le=1.0, description="Calculated metric of operational impact")

class SystemStatusResponse(BaseModel):
    status: str = Field(default="healthy")
    app_name: str
    environment: str
    active_monitors: List[str] = []