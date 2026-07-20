import sys
from pathlib import Path

# Ensure project root directory is in sys.path so 'backend' package imports work from any working directory
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api.endpoints import router as api_router
from backend.utils.error_handlers import global_exception_handler, SupplyChainAppException
from backend.utils.logging_utils import logger

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        debug=settings.DEBUG
    )
    
    # Configure baseline cross-origin security headers (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict this to specific origins in staging/production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Bind global application-wide exception handling middleware
    app.add_exception_handler(SupplyChainAppException, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    
    # Mount the modular API routes under versioned paths
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    logger.info("Application lifecycle initialization sequences completed successfully.")
    return app

app = create_application()