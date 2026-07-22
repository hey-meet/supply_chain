from typing import TypedDict

from backend.models.executive_summary import ExecutiveSummary
from backend.models.impact import ImpactAnalysis
from backend.models.mitigation import MitigationPlan
from backend.models.news_filter import FilteredNewsCollection
from backend.models.risk import RiskAnalysis
from backend.models.search import NewsCollection
from backend.models.agent_contracts import StructuredNews

class SupplyChainState(TypedDict, total=False):
    """
    Shared workflow state passed between LangGraph nodes.

    Each node reads from the state, performs one responsibility,
    and writes its output back into the state.
    """

    # Input
    query: str

    # Search
    search_results: NewsCollection

    # News Processing
    filtered_news: StructuredNews

    # Risk Analysis
    risk_analysis: RiskAnalysis

    # Business Impact
    impact_analysis: ImpactAnalysis

    # Mitigation Planning
    mitigation_plan: MitigationPlan

    # Executive Reporting
    executive_summary: ExecutiveSummary