# backend/api/endpoints.py

import uuid
from fastapi import APIRouter, BackgroundTasks
from backend.config import settings
from backend.api.schemas import SystemStatusResponse
from backend.api.inputs import DisruptionTelemetryInput
from backend.utils.workers import process_async_news_ingestion


# ==============================
# Import Modular Route Files
# ==============================
from backend.api.routes.news import router as news_router
from backend.api.routes.inventory import router as inventory_router
from backend.api.routes.incident import router as incident_router
from backend.api.routes.supply_chain import router as supply_chain_router
from backend.api.routes.decision_center import router as decision_center_router
from backend.api.routes.report import router as report_router
from backend.api.routes.dashboard import router as dashboard_router
from backend.api.routes.settings import router as settings_router
# SINGLE INITIALIZATION: Router defined once at the top (Fixes reviewer/Meet notes)
router = APIRouter()

# ==========================================
# Register Feature-Specific API Route Modules
# ==========================================
# All endpoints inside backend/api/routes/news.py
# will automatically be available under:
# /api/v1/news   (or /api/news depending on API_V1_STR)
router.include_router(news_router)
router.include_router(inventory_router)
router.include_router(incident_router)
router.include_router(supply_chain_router)
router.include_router(decision_center_router)
router.include_router(report_router)
router.include_router(dashboard_router)
router.include_router(settings_router)

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    """Get core system application health metrics and active streams."""
    return SystemStatusResponse(
        app_name=settings.APP_NAME,
        environment="development" if settings.DEBUG else "production",
        active_monitors=["tavily_news_stream"]
    )


@router.post("/telemetry/validate", status_code=201)
async def validate_incoming_telemetry(payload: DisruptionTelemetryInput):
    """
    Ingest raw shipment telemetry payloads.
    Applies regex data sanitization and coordinate constraints at the schema layer.
    """
    return {
        "success": True,
        "sanitized_tracking_id": payload.tracking_id,
        "message": "Input telemetry passed validation boundaries safely."
    }


@router.post("/news/ingest-async", status_code=202)
async def ingest_news_asynchronously(raw_text: str, background_tasks: BackgroundTasks):
    """
    Ingest heavy unstructured news content asynchronously.
    Returns HTTP 202 Accepted instantly to keep connection pools clear.
    """
    generated_id = str(uuid.uuid4())

    # Enqueue the processing task to run concurrently in the background worker queue
    background_tasks.add_task(process_async_news_ingestion, generated_id, raw_text)

    return {
        "success": True,
        "payload_id": generated_id,
        "status": "Processing initiated in background task queue."
    }