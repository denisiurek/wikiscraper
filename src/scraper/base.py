from abc import ABC, abstractmethod
import requests

class WikiScraper(ABC):
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.headers)

    def fetch_page(self, subpage: str) -> str:
        url = self._fetch_url(subpage)

        try:
            response = self.session.get(url, timeout = self.config.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError:
            raise ValueError(f"Page not found: {url}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request error for {url}: {e}")


    @abstractmethod
    def _fetch_url(self, search_phrase: str) -> str:

        pass

    @abstractmethod
    def parse_summary(self, html_content: str) -> str:

        pass

    @abstractmethod
    def extract_tables(self, html_content: str) -> list:

        pass

    @abstractmethod
    def fetch_page_redirections(self, url: str) -> list[str]:

        pass

    @abstractmethod
    def get_clean_text(self, html_content: str) -> str:

        pass