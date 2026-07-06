# backend/api/endpoints.py
from fastapi import APIRouter
from backend.config import settings
from backend.api.schemas import SystemStatusResponse

router = APIRouter()

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    return SystemStatusResponse(
        app_name=settings.APP_NAME,
        environment="development" if settings.DEBUG else "production",
        active_monitors=["tavily_news_stream"]
    )