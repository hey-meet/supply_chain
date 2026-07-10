# backend/api/endpoints.py
from fastapi import APIRouter
from backend.config import settings
from backend.api.schemas import SystemStatusResponse
# Append this to backend/api/endpoints.py
from fastapi import HTTPStatus
from backend.api.inputs import DisruptionTelemetryInput
# backend/api/endpoints.py
from fastapi import APIRouter
from backend.config import settings
from backend.api.schemas import SystemStatusResponse
from backend.api.inputs import DisruptionTelemetryInput
# Append this to backend/api/endpoints.py
from fastapi import BackgroundTasks, UUID4
import uuid
from backend.utils.workers import process_async_news_ingestion

@router.post("/news/ingest-async", status_code=202)
async def ingest_news_asynchronously(raw_text: str, background_tasks: BackgroundTasks):
    """
    Ingest heavy unstructured news content asynchronously.
    Returns HTTP 202 Accepted instantly to keep connection pools clear.
    """
    generated_id = str(uuid.uuid4())
    
    # Enqueue the processing task to run concurrently in the background
    background_tasks.add_task(process_async_news_ingestion, generated_id, raw_text)
    
    return {
        "success": True,
        "payload_id": generated_id,
        "status": "Processing initiated in background task queue."
    }

# FIX: Initialized at the top before any decorators use it
router = APIRouter()

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    return SystemStatusResponse(
        app_name=settings.APP_NAME,
        environment="development" if settings.DEBUG else "production",
        active_monitors=["tavily_news_stream"]
    )

@router.post("/telemetry/validate", status_code=201)
async def validate_incoming_telemetry(payload: DisruptionTelemetryInput):
    """
    Ingest raw shipment telemetry payloads.
    Applies regex sanitization and coordinate constraints at the schema layer.
    """
    return {
        "success": True,
        "sanitized_tracking_id": payload.tracking_id,
        "message": "Input telemetry passed validation boundaries safely."
    }

@router.post("/telemetry/validate", status_code=201)
async def validate_incoming_telemetry(payload: DisruptionTelemetryInput):
    """
    Ingest raw shipment telemetry payloads.
    Applies regex sanitization and coordinate constraints at the schema layer.
    """
    # At this point, payload data is 100% sanitized and typed-checked by your Pydantic layer
    return {
        "success": True,
        "sanitized_tracking_id": payload.tracking_id,
        "message": "Input telemetry passed validation boundaries safely."
    }


router = APIRouter()

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    return SystemStatusResponse(
        app_name=settings.APP_NAME,
        environment="development" if settings.DEBUG else "production",
        active_monitors=["tavily_news_stream"]
    )