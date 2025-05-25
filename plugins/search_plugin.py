from models import News, Search
from typing import Annotated, List
from services import DuckDuckGoService
from semantic_kernel.functions import kernel_function
from semantic_kernel import Kernel
from tools import spinner

class SearchPlugin:
    """Plugin for web searching."""
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.search_service = DuckDuckGoService()

    @spinner("Searching for company news")
    @kernel_function(description="Search the web for company news")
    def search_company_news(self, company_name: str) -> Annotated[List[News], "List of news articles related to the company."]:
        """Searches for news articles related to a specific company."""
        return self.search_service.search_news(company_name)
    
    @spinner("Searching the web")
    @kernel_function(description="Search the web for given text")
    def search_text(self, text: str) -> Annotated[List[Search], "List of searches related to the text."]:
        """Searches web for articles with given text"""
        return self.search_service.search_text(text)
    
