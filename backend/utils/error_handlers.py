# backend/utils/error_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from backend.utils.logging_utils import logger

class SupplyChainAppException(Exception):
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, SupplyChainAppException):
        logger.error(f"Application Error: {exc.message} | Details: {exc.details}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message, "details": exc.details}
        )
    
    logger.critical(f"Unhandled System Panic Encountered: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal Server Exception Encountered"}
    )