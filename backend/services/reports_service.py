# Week 4 Day 1: Production Calculations for Executive Financial Impact Reports
def generate_executive_impact_summary(disruptions: list) -> dict:
    total_loss = sum(d.get("estimated_loss", 0) for d in disruptions)
    affected_plants = len(set(d.get("plant_id") for d in disruptions if "plant_id" in d))
    
    return {
        "total_financial_impact": total_loss,
        "affected_facility_count": affected_plants,
        "impact_severity": "HIGH" if total_loss > 500000 else "MODERATE"
    }
