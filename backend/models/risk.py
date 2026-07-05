from pydantic import BaseModel


class RiskClassification(BaseModel):
    risk_type: str
    severity: str
    confidence: float