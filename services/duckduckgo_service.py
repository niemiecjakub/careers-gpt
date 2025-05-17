from duckduckgo_search import DDGS
from typing import List, Annotated
from models import NewsSearch
from pydantic import Field

class DuckDuckGoService:

    def search_news(self, keywords: str) -> Annotated[List[NewsSearch], Field(description="List of news articles related to the keywords.")]:
        articles = DDGS().news(keywords, max_results=5, timelimit="m")
        return [NewsSearch(**article) for article in articles]