from datetime import datetime, timezone

from backend.models.risk import RiskAnalysis, RiskAssessment, RiskCategory
from backend.models.search import SearchResult
from backend.prompts.risk_classifier import build_risk_classification_prompt
from backend.services.llm_client import LLMClient


class RiskClassificationAgent:
    """Agent responsible for preparing structured risk context from news articles."""

    def __init__(self):
        self.llm = LLMClient()

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
                "rain", "flood", "cyclone", "storm", "weather", "monsoon"
            ],
            RiskCategory.TRANSPORTATION: [
                "transport", "truck", "rail", "railway", "road", "highway",
                "shipping", "logistics"
            ],
            RiskCategory.RAW_MATERIAL_SHORTAGE: [
                "coal", "limestone", "gypsum", "fly ash", "raw material"
            ],
            RiskCategory.SUPPLIER_FAILURE: [
                "supplier", "shutdown", "bankruptcy", "closure"
            ],
            RiskCategory.LABOR_STRIKE: [
                "strike", "union", "worker", "labor"
            ],
            RiskCategory.REGULATORY: [
                "government", "regulation", "policy", "compliance"
            ],
            RiskCategory.PORT_CONGESTION: [
                "port", "harbor", "container", "vessel"
            ],
            RiskCategory.ENERGY: [
                "fuel", "diesel", "electricity", "power", "gas"
            ],
            RiskCategory.PRICE_FLUCTUATION: [
                "price", "inflation", "cost", "tariff"
            ],
            RiskCategory.GEOPOLITICAL: [
                "war", "conflict", "sanction", "border"
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

    def classify_risk(self, article: SearchResult) -> RiskAnalysis:
        """
        Extract features, run LLM-powered risk analysis, and return a validated 
        RiskAnalysis model.
        """
        # 1. Normalize published date and build prompt context
        published_date = self._normalize_published_date(article.published_date)
        context = self._build_context(article, published_date)
        
        prompt = build_risk_classification_prompt(context)

        # 2. Call LLM pipeline and validate output structured schema
        try:
            raw_response = self.llm.generate(prompt)
            
            # Clean potential markdown fences securely
            clean_response = (
                raw_response.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            assessment = RiskAssessment.model_validate_json(clean_response)

        except Exception as exc:
            raise RuntimeError(
                f"Failed to generate AI risk assessment: {exc}"
            ) from exc

        # 3. Construct and return final Pydantic model response
        return RiskAnalysis(
            news_id=str(article.url),
            headline=article.title,
            published_date=published_date,
            assessment=assessment,
        )

    def _build_context(self, article: SearchResult, published_date: datetime) -> dict:
        """Extract lightweight, structured context for token savings."""
        events = self.extract_key_events(article)
        summary = self.generate_summary(article)
        predicted_category = self.identify_disruption(events)

        return {
            "headline": article.title,
            "published_date": published_date.isoformat(),
            "summary": summary,
            "events": events,
            "predicted_category": predicted_category.value,
        }

    def _normalize_published_date(self, raw_date: str | None) -> datetime:
        """Safely parses incoming date strings or falls back to current UTC time."""
        if raw_date:
            try:
                return datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            except ValueError:
                pass
        return datetime.now(timezone.utc)