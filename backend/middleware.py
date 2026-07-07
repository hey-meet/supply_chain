# backend/middleware.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils.logging_utils import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Inbound Request: Method={request.method} Path={request.url.path}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(f"Outbound Response: Status={response.status_code} Performance={process_time:.4f}s")
        return response