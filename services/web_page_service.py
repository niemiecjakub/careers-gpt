import requests
from bs4 import BeautifulSoup

class WebPageService:
    """A service to fetch and parse HTML content from a given URL."""

    def get_html_content(self, url: str) -> str:
        """Fetches HTML content from a URL and extracts visible text."""
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        texts = [text.strip() for text in soup.stripped_strings if text.strip()]
        return '\n'.join(texts)
