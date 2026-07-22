import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.agents import risk_agent
from backend.agents.risk_agent import RiskClassificationAgent
from backend.models.search import SearchResult


def main():
    print("=" * 60)
    print("SUPPLY CHAIN AI RISK PIPELINE TEST")
    print("=" * 60)

    article = SearchResult(
        title="Heavy rainfall disrupts coal transportation across western India",
        url="https://example.com/news/coal-disruption",
        published_date="2026-07-07T10:30:00Z",
        content=(
            "Heavy rainfall caused severe flooding across western India. "
            "Coal transportation has been disrupted due to highway closures. "
            "Several cement manufacturers may face delays in raw material deliveries. "
            "Logistics companies are rerouting shipments."
        ),
        score=0.95,
    )

    print("\n[1] SearchResult created successfully")
    print(article)

    agent = RiskClassificationAgent()

    print("\n[2] RiskClassificationAgent initialized")

    print("\nFirst normalization of enum casing: ")
    articles = agent._normalize_enum_casing(article)
    print(articles)

    print("\n[3] Extracting key events...")
    events = agent.extract_key_events(article)
    print(events)

    print("\n[5] Predicting disruption category...")
    category = agent.identify_disruption(events)
    print(category)

    print("\n[6] Running full AI pipeline...")
    result = agent.classify_risks([article])

    print("\n[7] AI Risk Analysis Completed")

    if result:
        print(result[0].model_dump_json(indent=2))
    else:
        print("No results generated")

    print("\n")
    print("=" * 60)
    print("PIPELINE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()

    except Exception as exc:
        print("\n")
        print("=" * 60)
        print("PIPELINE TEST FAILED")
        print("=" * 60)
        print(type(exc).__name__)
        print(exc)
        raise
