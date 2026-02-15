import json
import os
from pathlib import Path

from dotenv import load_dotenv


def _load_api_keys(keys_path: Path) -> dict:
    load_dotenv(keys_path)
    return {
        key: value
        for key, value in os.environ.items()
        if key.endswith("KEY")
    }


def _default_config() -> dict:
    return {
        "wiki_url": "https://stardewvalleywiki.com",
        "user_agent": "WikiScraper/0.1.0",
        "word_freq_lang": "en",
        "json_path": "./word-counts.json",
        "mode": "stardew_normal",
        "is_debug": 0
    }


class ConfigLoader:
    def __init__(self, config_path: Path = Path("./config.json"), keys_path: Path = Path("./env")):
        self.path = Path(config_path).expanduser()
        self.base_dir = self.path.resolve().parent if self.path.exists() else Path.cwd().resolve()
        self.config = self._load()
        self._api_keys = _load_api_keys(keys_path)

    def _load(self) -> dict:

        config = _default_config()

        if self.path.exists():
            try:
                with open(self.path, "r", encoding='utf-8') as f:
                    user_config = json.load(f)
                    config.update(user_config)
            except json.JSONDecodeError:
                print(f"Warning: {self.path} contains invalid JSON. Using defaults.")
        else:
            print(f"Warning: {self.path} not found. Using defaults.")
        return config

    def _resolve_path(self, value: str | os.PathLike | None) -> Path:
        if value is None:
            return self.base_dir
        p = Path(value).expanduser()
        if p.is_absolute():
            return p
        return (self.base_dir / p).resolve()

    @property
    def wiki_url(self) -> str:
        return self.config.get("wiki_url")

    @property
    def headers(self) -> dict:
        return {"User-Agent": self.config.get("user_agent")}

    @property
    def is_debug(self) -> bool:
        return self.config.get("is_debug")

    @property
    def mode(self) -> str:
        return self.config.get("mode")

    @property
    def timeout(self) -> int:
        return self.config.get("request_timeout")

    @property
    def json_path(self) -> Path:
        return self._resolve_path(self.config.get("json_path"))

    @property
    def word_freq_lang(self) -> str:
        return self.config.get("word_freq_lang")

    @property
    def api_keys(self) -> dict:
        return self._api_keys

    @property
    def html_path(self) -> Path:
        return self._resolve_path(self.config.get("html_path"))
