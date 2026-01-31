import os

import json
from pathlib import Path
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path: str = "config.json", keys_path: str = ".env"):
        self.path = Path(config_path)
        self.keys_path = Path(keys_path)
        self.config = self._load()
        self._api_keys = self._load_api_keys()


    def _default(self) -> dict:
        return {
            "wiki_url": "https://stardewvalleywiki.com",
            "request_timeout": 10,
            "user_agent": "WikiScraper/1.0",
            "accept-language": "en-US,en;q=0.9",
            "mode": "stardew_normal"
        }


    def _load(self) -> dict:

        config = self._default()

        if self.path.exists():
            try:
                with open(self.path, "r", encoding='utf-8') as f:
                    user_config = json.load(f)
                    config.update(user_config)
            except json.JSONDecodeError:
                print(f"Warning: {self.path} contains invalid JSON. Using defaults.")
        return config


    def _load_api_keys(self) -> dict:
        load_dotenv()
        return {
            key: value
            for key, value in os.environ.items()
            if key.endswith("API_KEY")
        }


    @property
    def wiki_url(self) -> str:
        return self.config.get("wiki_url")

    @property
    def headers(self) -> dict:
        return {"User-Agent": self.config.get("user_agent"),
                "Accept-Language": self.config.get("accept_language")}

    @property
    def mode(self) -> str:
        return self.config.get("mode")

    @property
    def timeout(self) -> int:
        return self.config.get("request_timeout")
    @property
    def api_keys(self) -> dict:
        return self.config.get("api_keys", {})

    def __repr__(self):

        masked_keys = {}
        for service, key in self._api_keys.items():
            if key:
                masked_keys[service] = f"{key[:4]}...******"
            else:
                masked_keys[service] = "Missing key"

        return f"<Config = {self.config}, ConfigLoader keys = {masked_keys}>"