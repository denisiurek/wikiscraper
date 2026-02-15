from abc import ABC, abstractmethod

import pandas as pd
import requests


class WikiScraper(ABC):
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.headers)

    def fetch_page(self, subpage: str) -> str:
        try:
            url = self._fetch_url(subpage)
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request error for {subpage}: {e}")

    @abstractmethod
    def _fetch_url(self, search_phrase: str) -> str:
        pass

    @abstractmethod
    def parse_summary(self, html_content: str) -> str:
        pass

    @abstractmethod
    def extract_all_words(self, html_content: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def extract_tables(self, html_content: str) -> list:
        pass

    @abstractmethod
    def fetch_page_redirections(self, url: str) -> list[str]:
        pass
