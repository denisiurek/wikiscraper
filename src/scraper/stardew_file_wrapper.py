from pathlib import Path


from .stardew import StardewScraper


class StardewFileScraper(StardewScraper):
    def __init__(self, config):
        super().__init__(config)
        self.html_path = Path(config.html_path).resolve()
        if not self.html_path.exists():
            base_dir = getattr(config, 'base_dir', 'unknown')
            raise FileNotFoundError(
                f"Configured html_path does not exist: {self.html_path} "
                f"(config base_dir: {base_dir})"
            )

    def fetch_page(self, subpage: str) -> str:
        path = self._fetch_url(subpage)
        if not path.exists():
            raise FileNotFoundError(f"Local HTML file not found for '{subpage}': {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _fetch_url(self, search_phrase: str) -> Path:
        return self.html_path / Path(search_phrase.strip().replace(" ", "_") + ".html")
