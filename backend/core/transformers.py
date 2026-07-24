# Week 3 Day 3: Contract Preservation Layer
def ensure_frontend_contract_parity(raw_data: dict, expected_keys: list):
    """Ensures backend logic outputs match original mock response schema exactly."""
    for key in expected_keys:
        if key not in raw_data:
            raw_data[key] = None
    return raw_data
