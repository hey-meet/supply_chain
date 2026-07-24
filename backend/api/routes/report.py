# backend/api/routes/report.py

import time
import logging
from fastapi import APIRouter
from backend.services.graph_service import graph_service
from backend.services.response_transformer import transform_reports

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/reports",
    tags=["Executive Reports"]
)

@router.get("")
async def get_executive_reports():
    start_time = time.perf_counter()
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
        
    transform_start = time.perf_counter()
    response = transform_reports(cache.workflow_state)
    transform_time = time.perf_counter() - transform_start
    
    api_time = time.perf_counter() - start_time
    logger.info(
        "Reports Endpoint Performance: Transform: %.4fs, API: %.4fs",
        transform_time,
        api_time
    )
    
    if response.get("success") and "data" in response:
        response["data"]["metrics"] = {
            "transform_time_seconds": round(transform_time, 4),
            "api_response_time_seconds": round(api_time, 4)
        }
        
    return response