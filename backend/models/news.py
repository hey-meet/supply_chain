from pydantic import BaseModel


class NewsArticle(BaseModel):
    title: str
    content: str
    source: str
    url: str