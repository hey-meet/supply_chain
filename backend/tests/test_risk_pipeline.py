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

    print("\n[3] Extracting key events...")
    events = agent.extract_key_events(article)
    print(events)

    print("\n[4] Generating summary...")
    summary = agent.generate_summary(article)
    print(summary)

    print("\n[5] Predicting disruption category...")
    category = agent.identify_disruption(events)
    print(category)

    print("\n[6] Running full AI pipeline...")
    result = agent.classify_risk(article)

    print("\n[7] AI Risk Analysis Completed")

    print(result.model_dump_json(indent=2))

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