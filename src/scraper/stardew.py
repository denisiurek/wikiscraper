from .base import WikiScraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re

class StardewScraper(WikiScraper):
    def __init__(self, config):
        super().__init__(config)

    def _fetch_url(self, search_phrase: str) -> str:
        formatted_phrase = search_phrase.strip().replace(" ", "_")
        return f"{self.base_url}/{formatted_phrase}"

    def parse_summary(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')

        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            return "No content found."

        paragraphs = content_div.find_all("p")
        for p in paragraphs:
            raw_text = p.get_text(" ", strip=True)
            clean_text = raw_text.replace(" .", ".").replace(" '", "'")
            if len(raw_text) > 20:

                return ' '.join(clean_text.split())

        return "No summary paragraph found."

    def extract_tables(self, html_content: str) -> list:
        pass

    def fetch_page_redirections(self, url: str) -> list[str]:
        pass

    def get_clean_text(self, html_content: str) -> str:
        pass