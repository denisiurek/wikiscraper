import json
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path: str = "config.json"):
        self.path = Path(config_path)
        self.config = self._load()

    def _default(self) -> dict:
        """Returns the hardcoded default configuration."""
        return {
            "wiki_url": "https://stardewvalleywiki.com",
            "request_timeout": 10,
            "user_agent": "WikiScraper/1.0"
        }

    def _load(self) -> dict:
        """Loads config from file, falling back to defaults if file is missing."""
        config = self._default()

        if self.path.exists():
            try:
                with open(self.path, "r", encoding='utf-8') as f:
                    user_config = json.load(f)
                    config.update(user_config)
            except json.JSONDecodeError:
                print(f"Warning: {self.path} contains invalid JSON. Using defaults.")
        return config

    @property
    def wiki_url(self) -> str:
        return self.config.get("wiki_url")

    @property
    def headers(self) -> dict:
        return {"User-Agent": self.config.get("user_agent")}