from pydantic import BaseModel

class NewsAgentInput(BaseModel):
    query: str

class StructuredNews(BaseModel):
    title: str
    content: str
    source: str
    published_at: str

class RiskAgentInput(BaseModel):
    articles: list[StructuredNews]