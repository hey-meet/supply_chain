from pydantic import BaseModel, HttpUrl


class SearchResult(BaseModel):
    """Represents a single news search result."""

    title: str
    url: HttpUrl
    published_date: str | None = None
    content: str
    score: float


class NewsCollection(BaseModel):
    """Collection of news search results."""

    query: str
    results: list[SearchResult]