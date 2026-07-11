from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from backend.models.location import Location


class NewsArticle(BaseModel):
    """Represents a processed news article ready for AI analysis."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    title: str = Field(
        ...,
        min_length=1,
        description="Article title",
    )

    content: str = Field(
        ...,
        min_length=1,
        description="Cleaned article content",
    )

    source: str | None = Field(
        default=None,
        description="News source or publisher",
    )

    url: HttpUrl = Field(
        ...,
        description="Original article URL",
    )

    published_date: str | None = Field(
        default=None,
        description="Publication date",
    )

    location: Location | None = Field(
        default=None,
        description="Extracted location information",
    )

    search_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Search relevance score",
    )