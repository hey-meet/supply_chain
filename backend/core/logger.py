import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("supply_chain_backend")

def log_api_error(endpoint: str, error_msg: str):
    logger.error(f"[API Error] Path: {endpoint} | Details: {error_msg}")
