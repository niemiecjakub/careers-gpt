from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class News(BaseModel):
    date: datetime = Field(..., description="ISO 8601 formatted datetime string")
    title: str = Field(..., min_length=1, description="Title of the news article")
    body: str = Field(..., min_length=1, description="Content of the news article")
    url: HttpUrl = Field(..., description="URL to the full news article")
    source: str = Field(..., min_length=1, description="Source or publisher of the news")

class Search(BaseModel):
    title: str = Field(..., description="The title of the search result (e.g., the page or article headline)")
    href: HttpUrl = Field(..., description="The URL of the search result (must be a valid HTTP/HTTPS URL)")
    body: str = Field(..., description="A brief summary or snippet from the content of the result")
