from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class NewsSearch(BaseModel):
    date: datetime = Field(..., description="ISO 8601 formatted datetime string")
    title: str = Field(..., min_length=1, description="Title of the news article")
    body: str = Field(..., min_length=1, description="Content of the news article")
    url: HttpUrl = Field(..., description="URL to the full news article")
    source: str = Field(..., min_length=1, description="Source or publisher of the news")
