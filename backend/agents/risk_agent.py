from backend.models.risk import RiskCategory
from backend.models.search import SearchResult


class RiskClassificationAgent:
    """Agent responsible for preparing structured risk context from news articles."""

    def extract_key_events(self, article: SearchResult) -> list[str]:
        """
        Extract key events from the news content.

        Current implementation:
        - Split content into sentences.
        - Remove empty sentences.
        """

        sentences = [
            sentence.strip()
            for sentence in article.content.replace("\n", " ").split(".")
            if sentence.strip()
        ]

        return [f"{sentence}." for sentence in sentences]

    def identify_disruption(self, events: list[str]) -> RiskCategory:
        """
        Perform simple keyword-based disruption classification.

        This serves as a temporary implementation until the LLM
        performs semantic classification.
        """

        text = " ".join(events).lower()

        keyword_mapping = {
            RiskCategory.WEATHER: [
                "rain",
                "flood",
                "cyclone",
                "storm",
                "weather",
                "monsoon",
            ],
            RiskCategory.TRANSPORTATION: [
                "transport",
                "truck",
                "rail",
                "railway",
                "road",
                "highway",
                "shipping",
                "logistics",
            ],
            RiskCategory.RAW_MATERIAL_SHORTAGE: [
                "coal",
                "limestone",
                "gypsum",
                "fly ash",
                "raw material",
            ],
            RiskCategory.SUPPLIER_FAILURE: [
                "supplier",
                "shutdown",
                "bankruptcy",
                "closure",
            ],
            RiskCategory.LABOR_STRIKE: [
                "strike",
                "union",
                "worker",
                "labor",
            ],
            RiskCategory.REGULATORY: [
                "government",
                "regulation",
                "policy",
                "compliance",
            ],
            RiskCategory.PORT_CONGESTION: [
                "port",
                "harbor",
                "container",
                "vessel",
            ],
            RiskCategory.ENERGY: [
                "fuel",
                "diesel",
                "electricity",
                "power",
                "gas",
            ],
            RiskCategory.PRICE_FLUCTUATION: [
                "price",
                "inflation",
                "cost",
                "tariff",
            ],
            RiskCategory.GEOPOLITICAL: [
                "war",
                "conflict",
                "sanction",
                "border",
            ],
        }

        for category, keywords in keyword_mapping.items():
            if any(keyword in text for keyword in keywords):
                return category

        return RiskCategory.OTHER

    def generate_summary(self, article: SearchResult) -> str:
        """
        Generate a lightweight summary.

        Current implementation:
        Return the first two sentences.
        """

        events = self.extract_key_events(article)

        if not events:
            return ""

        return " ".join(events[:2])

    def classify_risk(self, article: SearchResult) -> dict:
        """
        Prepare structured context for downstream LLM analysis.

        Returns:
            dict containing headline, summary, extracted events,
            predicted category, and original content.
        """

        events = self.extract_key_events(article)
        category = self.identify_disruption(events)
        summary = self.generate_summary(article)

        return {
            "headline": article.title,
            "summary": summary,
            "events": events,
            "predicted_category": category,
            "content": article.content,
        }