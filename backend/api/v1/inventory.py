from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/inventory", tags=["Inventory"])

class InventoryItem(BaseModel):
    item_id: str
    plant_id: str
    stock_level: int

@router.get("/{item_id}", response_model=InventoryItem)
async def get_inventory(item_id: str):
    return {"item_id": item_id, "plant_id": "PLANT-01", "stock_level": 5000}
