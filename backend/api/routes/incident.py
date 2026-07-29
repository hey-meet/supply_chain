# backend/api/routes/incident.py

import time
import logging
from datetime import datetime, timezone
from fastapi import APIRouter
from backend.services.graph_service import graph_service
from backend.services.response_transformer import transform_incident

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/incident",
    tags=["Incident Center"]
)

@router.get("")
def get_incident_center(query: str | None = None):
    start_time = time.perf_counter()
    
    if query:
        # Trigger dynamic LangGraph pipeline execution
        graph_service.execute_pipeline(query)
        
    cache = graph_service.get_cache()
    
    if not cache.is_initialized:
        api_time = time.perf_counter() - start_time
        return {
            "success": False,
            "message": "Analysis pending. Please execute a query first.",
            "data": {},
            "metrics": {
                "api_response_time_seconds": round(api_time, 4)
            }
        }
        
    # Transform workflow state
    transform_start = time.perf_counter()
    response = transform_incident(cache.workflow_state)
    transform_time = time.perf_counter() - transform_start
    
    api_time = time.perf_counter() - start_time
    logger.info(
        "Incident Endpoint Performance: GraphExec: %.4fs, Transform: %.4fs, API: %.4fs",
        cache.graph_execution_time_seconds,
        transform_time,
        api_time
    )
    
    if response.get("success") and "data" in response:
        response["data"]["metrics"] = {
            "graph_execution_time_seconds": round(cache.graph_execution_time_seconds, 4),
            "transform_time_seconds": round(transform_time, 4),
            "api_response_time_seconds": round(api_time, 4)
        }
        
    return response