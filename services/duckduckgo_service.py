from duckduckgo_search import DDGS
from typing import List, Annotated
from models import News, Search
from pydantic import Field

class DuckDuckGoService:

    def search_news(self, keywords: str) -> Annotated[List[News], Field(description="List of news articles related to the keywords.")]:
        articles = DDGS().news(keywords, max_results=5, timelimit="m")
        return [News(**article) for article in articles]

    def search_text(self, text: str) -> Annotated[List[Search], Field(description="List of searches related to the text")]:
        searches = DDGS().text(text, max_results=5, timelimit="m")
        return [Search(**search) for search in searches]
