from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/plants", tags=["Plants & Network"])

class PlantStatus(BaseModel):
    plant_id: str
    operational_status: str
    capacity_utilization: float

@router.get("/{plant_id}", response_model=PlantStatus)
async def get_plant_metrics(plant_id: str):
    return {"plant_id": plant_id, "operational_status": "active", "capacity_utilization": 0.84}
