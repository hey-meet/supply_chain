# backend/tests/test_api_integration.py

from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.search import NewsCollection, SearchResult
from backend.services.graph_service import graph_service

client = TestClient(app)

def test_api_endpoints_integration():
    """
    Integration test validating standard cache flow and response mapping.
    """
    # Force reset the cache
    graph_service._cache = graph_service._cache.__class__()

    # 1. Fetch incident center when cache is uninitialized
    resp = client.get("/api/v1/incident")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["success"] is False
    assert "pending" in payload["message"]

    # 2. Mock Tavily search result to return Rajasthan limestone disruption
    mock_news_collection = NewsCollection(
        query="Heavy rainfall Jodhpur",
        results=[
            SearchResult(
                title="Monsoons inundate Marwar Mining quarry Jodhpur",
                url="https://example.com/news/marwar-disruption",
                published_date="2026-07-23T10:30:00Z",
                content=(
                    "Heavy monsoon rainfall has caused severe flooding in Jodhpur, Rajasthan. "
                    "Marwar Mining & Minerals Corp. has suspended all limestone aggregate quarrying. "
                    "Transportation routes leaving the site are completely blocked."
                ),
                score=0.95
            )
        ]
    )

    # Trigger integration execution with mock Tavily search
    with patch('backend.agents.news_agent.NewsIntelligenceAgent.fetch_news', return_value=mock_news_collection):
        resp = client.get("/api/v1/incident?query=Heavy+rainfall+Jodhpur")
        assert resp.status_code == 200
        payload = resp.json()
        assert payload["success"] is True
        assert "incident_meta" in payload["data"]
        
        meta = payload["data"]["incident_meta"]
        assert meta["severity"] == "High"
        assert meta["location"] in ["Jodhpur", "Rajasthan Region"]
        assert "Marwar Mining" in meta["description"] or "Marwar" in meta["description"] or "limestone" in meta["description"]

    # 3. Verify downstream routes pull transformed data from the cache
    resp_news = client.get("/api/v1/api/news")
    assert resp_news.status_code == 200
    news_payload = resp_news.json()
    assert news_payload["success"] is True
    assert len(news_payload["data"]["news_feed"]) > 0

    resp_inv = client.get("/api/v1/inventory")
    assert resp_inv.status_code == 200
    inv_payload = resp_inv.json()
    assert inv_payload["success"] is True
    # Verify the Jodhpur plant is At Risk / Warning
    plants = inv_payload["data"]["plants"]
    jodhpur_plant = next((p for p in plants if p["id"] == "PLT-001"), None)
    assert jodhpur_plant is not None
    assert jodhpur_plant["status"] in ["At Risk", "Warning"]

    resp_sc = client.get("/api/v1/supply-chain")
    assert resp_sc.status_code == 200
    sc_payload = resp_sc.json()
    assert sc_payload["success"] is True
    assert len(sc_payload["data"]["nodes"]) > 0

    resp_dc = client.get("/api/v1/decision-center")
    assert resp_dc.status_code == 200
    dc_payload = resp_dc.json()
    assert dc_payload["success"] is True

    resp_rep = client.get("/api/v1/reports")
    assert resp_rep.status_code == 200
    rep_payload = resp_rep.json()
    assert rep_payload["success"] is True

    # 4. Verify dashboard endpoint is pending when uninitialized, and maps correctly when initialized
    # Uninitialized dashboard check (reset cache first)
    graph_service._cache = graph_service._cache.__class__()
    resp_dash_uninit = client.get("/api/v1/dashboard")
    assert resp_dash_uninit.status_code == 200
    assert resp_dash_uninit.json()["success"] is False

    # Execute pipeline to initialize cache
    with patch('backend.agents.news_agent.NewsIntelligenceAgent.fetch_news', return_value=mock_news_collection):
        client.get("/api/v1/incident?query=Heavy+rainfall+Jodhpur")

    resp_dash = client.get("/api/v1/dashboard")
    assert resp_dash.status_code == 200
    dash_payload = resp_dash.json()
    assert dash_payload["success"] is True
    data = dash_payload["data"]
    assert len(data["kpis"]) > 0
    assert len(data["news_intelligence"]) > 0
    assert len(data["disruption_markers"]) > 0
    assert len(data["ai_recommendations"]) > 0
    assert "metrics" in data
    assert data["metrics"]["graph_execution_time_seconds"] >= 0.0
