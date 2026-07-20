# Week 3 Day 2: Advanced Incident Classification Engine
def classify_supply_chain_incident(severity_score: float):
    if severity_score >= 0.8:
        return "CRITICAL_DISRUPTION"
    elif severity_score >= 0.4:
        return "MODERATE_DELAY"
    return "NOMINAL"
