from fastapi import HTTPException, status

class ServiceLayerException(Exception):
    def __init__(self, message: str):
        self.message = message

def raise_network_timeout_boundary():
    raise HTTPException(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        detail="Downstream supply chain service failed to respond within threshold margins."
    )
