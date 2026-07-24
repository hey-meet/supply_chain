# backend/api/routes/news.py

import time
import logging
from fastapi import APIRouter
from backend.services.graph_service import graph_service
from backend.services.response_transformer import transform_news

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/news",
    tags=["News Intelligence"],
)

@router.get("")
async def get_news_intelligence():
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
    response = transform_news(cache.workflow_state)
    transform_time = time.perf_counter() - transform_start
    
    api_time = time.perf_counter() - start_time
    logger.info(
        "News Endpoint Performance: Transform: %.4fs, API: %.4fs",
        transform_time,
        api_time
    )
    
    if response.get("success") and "data" in response:
        response["data"]["metrics"] = {
            "transform_time_seconds": round(transform_time, 4),
            "api_response_time_seconds": round(api_time, 4)
        }
        
    return response

@router.get("/scan")
async def scan_today_news():
    start_time = time.perf_counter()
    try:
        from backend.services.search_service import search_service
        from backend.services.response_transformer import transform_news_from_scan
        
        # Execute scan
        news_feed = search_service.scan_today_news()
        
        # Transform news using the scanned news feed
        response = transform_news_from_scan(news_feed)
        
        api_time = time.perf_counter() - start_time
        if response.get("success") and "data" in response:
            response["data"]["metrics"] = {
                "api_response_time_seconds": round(api_time, 4)
            }
        return response
    except Exception as exc:
        logger.exception("Daily news scan failed: %s", exc)
        return {
            "success": False,
            "message": f"Daily news scan failed: {exc}",
            "data": {}
        }