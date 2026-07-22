import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.agents.news_agent import news_agent
from backend.models.search import NewsCollection, SearchResult

def test_fetch_news():
    response = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    assert isinstance(response, NewsCollection)
    assert response.query != ""
    assert isinstance(response.results, list)

if __name__ == "__main__":
    print("=" * 60)
    print("NEWS AGENT TEST")
    print("=" * 60)
    
    print("Fetching news for 'cement supply chain disruption'...")
    response = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )
    
    print(f"\nFetched {len(response.results)} articles.")
    for i, article in enumerate(response.results, 1):
        print(f"\nArticle {i}: {article.title}")
        print(f"URL: {article.url}")
        
    print("\n" + "=" * 60)
    print("TEST PASSED")
    print("=" * 60)
