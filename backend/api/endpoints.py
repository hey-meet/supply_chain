# backend/api/endpoints.py
import uuid
from fastapi import APIRouter, BackgroundTasks
from backend.config import settings
from backend.api.schemas import SystemStatusResponse
from backend.api.inputs import DisruptionTelemetryInput
from backend.utils.workers import process_async_news_ingestion

# SINGLE INITIALIZATION: Router defined once at the top (Fixes reviewer/Meet notes)
router = APIRouter()

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