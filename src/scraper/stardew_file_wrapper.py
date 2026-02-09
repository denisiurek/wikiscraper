from pathlib import Path

import pandas as pd

from . import StardewScraper
from . import WikiScraper


class StardewFileScraper(WikiScraper):
    def __init__(self, config):
        super().__init__(config)
        self.scraper = StardewScraper(config)

    def fetch_page(self, subpage: str) -> str:
        path = self._fetch_url(subpage)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _fetch_url(self, subpage: str) -> Path:
        return Path("./local_page/" + subpage.strip().replace(" ", "_") + ".html")

    def parse_summary(self, html_content: str) -> str:
        return self.scraper.parse_summary(html_content)

    def extract_all_words(self, html_content: str) -> pd.DataFrame:
        return self.scraper.extract_all_words(html_content)

    def extract_tables(self, html_content: str) -> list[pd.DataFrame]:
        return self.scraper.extract_tables(html_content)

    def fetch_page_redirections(self, html_content: str) -> list[str]:
        return self.scraper.fetch_page_redirections(html_content)
