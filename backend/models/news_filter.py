from pydantic import BaseModel, ConfigDict, Field

from backend.models.news import NewsArticle


class FilteredNewsCollection(BaseModel):
    """Collection of news articles filtered for relevance and duplicates."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    query: str = Field(
        ...,
        description="Search query used for fetching the news.",
    )

    articles: list[NewsArticle] = Field(
        default_factory=list,
        description="List of filtered news articles.",
    )
