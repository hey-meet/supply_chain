from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])

class IncidentPayload(BaseModel):
    incident_id: str
    node_impacted: str
    severity: str = Field(..., max_length=20)
