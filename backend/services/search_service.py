from backend.models.search import NewsCollection, SearchResult
from backend.services.tavily_client import tavily_client


class SearchService:
    """Service layer for retrieving logistics and supply chain news."""

    def search_news(
        self,
        query: str,
        max_results: int = 5,
    ) -> NewsCollection:
        """Search news using a custom query."""

        response = tavily_client.search(
            query=query,
            topic="news",
            max_results=max_results,
        )

        results = []

        for item in response.get("results", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url"),
                    published_date=item.get("published_date"),
                    content=item.get("content", ""),
                    score=item.get("score", 0.0),
                )
            )

        return NewsCollection(
            query=query,
            results=results,
        )

    def search_logistics_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve recent logistics-related news."""
        return self.search_news(
            query="latest logistics disruptions transportation freight shipping",
            max_results=max_results,
        )

    def search_supply_chain_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve recent supply chain news."""
        return self.search_news(
            query="latest supply chain disruptions cement manufacturing",
            max_results=max_results,
        )

    def search_weather_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve weather events affecting transportation and logistics."""
        return self.search_news(
            query="extreme weather affecting logistics transportation India",
            max_results=max_results,
        )

    def search_commodity_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve commodity market news relevant to cement manufacturing."""
        return self.search_news(
            query="coal diesel gypsum fly ash commodity price news",
            max_results=max_results,
        )

    def scan_today_news(self, max_results_per_query: int = 2) -> list[dict]:
        """Perform autonomous scan of today's supply chain news using config expressions."""
        import json
        import logging
        from pathlib import Path
        from datetime import datetime, timezone
        from backend.agents.news_agent import news_agent
        from backend.agents.news_filter_agent import news_filter_agent
        from backend.agents.risk_agent import RiskClassificationAgent
        
        logger = logging.getLogger(__name__)
        risk_agent = RiskClassificationAgent()

        # Load queries from config
        config_path = Path(__file__).resolve().parent.parent / "config" / "news_topics.json"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            queries = config_data.get("search_queries", [])
        except Exception as e:
            logger.error("Failed to load news topics config: %s. Using default fallback query.", e)
            queries = ["cement supply chain logistics disruption heavy rainfall flood strike port congestion closure"]

        # Run Tavily search for each query and collect all articles
        all_articles = []
        seen_urls = set()
        
        for q in queries:
            try:
                search_results = news_agent.fetch_news(query=q, max_results=max_results_per_query)
                for article in search_results.results:
                    url = str(article.url)
                    if url not in seen_urls:
                        seen_urls.add(url)
                        all_articles.append(article)
            except Exception as e:
                logger.error("Failed to fetch news for query %r: %s", q, e)
                
        # Limit total articles to filter to avoid performance/cost issues
        raw_collection = NewsCollection(
            query="Today's Autonomous Scan",
            results=all_articles[:10]  # Cap at 10 raw articles
        )
        
        # Filter relevant articles using news_filter_agent
        structured_news = news_filter_agent.prepare_agent_input(raw_collection)
        relevant_articles = structured_news.articles[:5]  # Cap at top 5 for risk classification
        
        # Classify risks using risk_agent
        search_results_for_risk = [
            SearchResult(
                title=article.title,
                content=article.content,
                url=article.url,
                published_date=article.published_date,
                score=article.search_score,
            )
            for article in relevant_articles
        ]
        
        risk_analyses = risk_agent.classify_risks(search_results_for_risk)
        
        news_feed = []
        for idx, risk in enumerate(risk_analyses):
            art = next((a for a in relevant_articles if str(a.url) == risk.news_id), None)
            
            category_val = risk.assessment.category.value
            severity_val = risk.assessment.severity.value.upper()
            confidence_val = f"{int(risk.assessment.confidence * 100)}%"
            
            location_str = "National Block"
            country_str = "India"
            state_str = "All"
            
            if risk.assessment.location:
                country_str = risk.assessment.location.country or "India"
                state_str = risk.assessment.location.state or "All"
                location_str = risk.assessment.location.city or "National Block"
                
            news_feed.append({
                "id": idx + 1,
                "publisher": (art.source if art else None) or "Global Logistics Wire",
                "initials": ((art.source if art else None) or "GL")[:2].upper(),
                "headline": risk.headline,
                "time": risk.published_date.strftime("%I:%M %p") if isinstance(risk.published_date, datetime) else "10:15 AM",
                "country": country_str,
                "state": state_str,
                "location": location_str,
                "summary": risk.assessment.summary,
                "entity": ", ".join(risk.assessment.affected_materials) if risk.assessment.affected_materials else "Primary Sourcing",
                "severity": severity_val,
                "confidence": confidence_val,
                "status": "Validated",
                "category": category_val,
                "material_impact": ", ".join(risk.assessment.affected_materials) if risk.assessment.affected_materials else "None"
            })
            
        return news_feed


search_service = SearchService()