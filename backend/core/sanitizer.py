# Week 4 Day 1: Backend Service Boundary Input Validation
def sanitize_service_payload(payload: dict) -> dict:
    cleaned = {}
    for key, value in payload.items():
        if isinstance(value, str):
            cleaned[key] = value.strip()
        else:
            cleaned[key] = value
    return cleaned
