import re
from io import StringIO
from string import punctuation
from urllib.parse import unquote

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .base import WikiScraper


class StardewScraper(WikiScraper):
    def __init__(self, config):
        super().__init__(config)

    def _fetch_url(self, search_phrase: str) -> str:
        formatted_phrase = search_phrase.strip().replace(" ", "_")
        url = f"{self.config.wiki_url}/{formatted_phrase}"
        response = requests.get(url)
        if response.status_code < 400:
            return url
        else:
            try:
                return self._fallback_fetch_url(search_phrase)
            except Exception as e:
                raise ValueError(f"Failed to fetch URL for '{search_phrase}': {e}")

    def parse_summary(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')

        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            raise ValueError("No content div found.")

        paragraphs = content_div.find_all("p")
        for p in paragraphs:
            raw_text = p.get_text(separator=" ", strip=True)
            clean_text = raw_text.replace(" .", ".").replace(" '", "'").replace(" ,", ",")
            if len(raw_text) > 30:
                return ' '.join(clean_text.split())

        raise ValueError("No suitable summary found.")

    def extract_tables(self, html_content: str) -> list[pd.DataFrame]:
        soup = BeautifulSoup(html_content, 'html.parser')
        found_tags = soup.find_all('table', {'class': re.compile(r'wikitable')})

        dfs = []
        for tag in found_tags:
            first_row = tag.find('tr')
            is_first_col_header = False
            if first_row:
                first_cell = first_row.find(['td', 'th'])
                if first_cell and first_cell.name == 'th':
                    is_first_col_header = True

            index_col_param = 0 if is_first_col_header else None
            df_list = pd.read_html(
                StringIO(str(tag)),
                header=0,
                index_col=index_col_param
            )
            if df_list:
                dfs.append(df_list[0])

        return dfs

    def extract_all_words(self, html_content: str) -> pd.DataFrame:
        soup = BeautifulSoup(html_content, 'html.parser')
        main_content = soup.find('div', id='mw-content-text')

        if not main_content:
            return pd.DataFrame(columns=['word'])

        for junk in main_content.find_all(['style', 'script']):
            junk.decompose()

        raw_text = main_content.get_text(separator=' ').lower()

        extra_punctuation = "“”„”«»–—"
        to_remove = punctuation.replace("'", "") + extra_punctuation

        table = str.maketrans(to_remove, ' ' * len(to_remove))
        clean_text = raw_text.translate(table)

        words_list = clean_text.split()

        filtered_words = [
            word.strip("'") for word in words_list
            if word.strip("'") and not word.isdigit() and len(word.strip("'")) > 1
        ]
        return pd.DataFrame(filtered_words, columns=['word'])

    def fetch_page_redirections(self, html_content: str) -> list[str]:
        soup = BeautifulSoup(html_content, 'html.parser')

        content_div = soup.select_one('div#mw-content-text')
        if not content_div:
            return []

        blocked_namespaces = { # some are unnecessary to block, but this is a good starting point imho
            'file', 'image', 'category', 'special', 'help', 'talk', 'user', 'user talk',
            'template', 'template talk', 'mediawiki', 'mediawiki talk', 'module',
            'module talk', 'portal', 'draft', 'timedtext', 'mailto', 'tel',
            'javascript', 'datei'
        }

        def process_href(href):
            if href.lower().startswith(('/#', '/wiki/#', '//')):
                return None

            path = href.split('#')[0].split('?')[0].lstrip('/')
            if not path:
                return None

            candidate = path.split('/', 1)[0]
            title = unquote(candidate).replace('_', ' ').strip()

            if not title:
                return None

            if ':' in title:
                ns = title.split(':', 1)[0].lower()
                if ns in blocked_namespaces:
                    return None

            return title

        raw_links = (a['href'] for a in content_div.select('a[href^="/"]'))

        titles = (process_href(href) for href in raw_links)

        return list(dict.fromkeys(t for t in titles if t is not None))

    def _google_api_handler(self, search_phrase: str) -> str:
        # Using Serper.dev API to search for the page URL on the wiki
        # Google deprecated custom search api for new clients
        url = "https://google.serper.dev/search"
        search_phrase = f"{search_phrase} site:{self.config.wiki_url}"
        payload = {
            "q": search_phrase
        }
        headers = {
            'X-API-KEY': self.config.api_keys["X-API-KEY"],
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, json=payload)

        results = response.json()
        if 'organic' in results and len(results['organic']) > 0:
            print(
                f"Site not found directly, used google search and got item {results['organic'][0]['title']}, verify validity")
            return results['organic'][0]['link']
        else:
            raise ValueError("No site found and fallback search failed.")

    def _fallback_fetch_url(self, search_phrase: str) -> str | None:
        try:
            return self._google_api_handler(search_phrase)
        except Exception as e:
            print(f"Google API search failed: {e}")
