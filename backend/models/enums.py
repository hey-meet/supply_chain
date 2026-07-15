from enum import Enum


class SeverityLevel(str, Enum):
    """Severity assigned by the Risk Classification Agent."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    """Supported supply chain disruption categories."""

    RAW_MATERIAL_SHORTAGE = "raw_material_shortage"
    TRANSPORTATION = "transportation"
    WEATHER = "weather"
    PORT_CONGESTION = "port_congestion"
    SUPPLIER_FAILURE = "supplier_failure"
    REGULATORY = "regulatory"
    LABOR_STRIKE = "labor_strike"
    ENERGY = "energy"
    PRICE_FLUCTUATION = "price_fluctuation"
    GEOPOLITICAL = "geopolitical"
    OTHER = "other"


class BusinessImpact(str, Enum):
    """Estimated business impact."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SEVERE = "severe"


class AgentStatus(str, Enum):
    """Overall status returned by AI agents."""

    SUCCESS = "success"
    FAILED = "failed"


class MatchReason(str, Enum):
    """Why a supplier was matched to a disruption."""

    NAME = "name"
    LOCATION = "location"
    NAME_AND_LOCATION = "name_and_location"
