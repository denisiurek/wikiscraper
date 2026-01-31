from .base import WikiScraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re

class StardewScraper(WikiScraper):

    def _fetch_url(self, search_phrase: str) -> str:
        formatted_phrase = search_phrase.strip().replace(" ", "_")
        return f"{self.base_url}/{formatted_phrase}"

    def parse_summary(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")

        content_div = soup.find(id="mw-content-text")
        if not content_div:
            raise ValueError("No content found")
        paragraphs = content_div.find_all("p")
        par0 = paragraphs[0].text if paragraphs else ""
        clean_text = re.sub(r'\[\d+\]', '', par0)
        return clean_text.strip()

    def extract_tables(self, html_content: str) -> list:
        pass

    def fetch_page_redirections(self, url: str) -> list[str]:
        pass

    def get_clean_text(self, html_content: str) -> str:
        pass