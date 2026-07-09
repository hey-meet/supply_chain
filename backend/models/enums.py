from enum import Enum


class SeverityLevel(str, Enum):
    """
    Severity assigned by the Risk Classification Agent.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    """
    Supply chain disruption categories.
    """

    WEATHER = "weather"
    LOGISTICS = "logistics"
    TRANSPORTATION = "transportation"
    SUPPLIER = "supplier"
    PORT = "port"
    RAW_MATERIAL = "raw_material"
    ENERGY = "energy"
    LABOR = "labor"
    REGULATORY = "regulatory"
    GEOPOLITICAL = "geopolitical"
    OTHER = "other"


class AgentStatus(str, Enum):
    """
    Overall status returned by AI agents.
    """

    SUCCESS = "success"
    FAILED = "failed"