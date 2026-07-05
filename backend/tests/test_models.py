from backend.models.news import NewsArticle
from backend.models.risk import RiskClassification
from backend.models.agent_response import AgentResponse


def test_import_models():
    assert NewsArticle
    assert RiskClassification
    assert AgentResponse