from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from wikiscraper import ConfigLoader
from wikiscraper import StardewFileScraper


@pytest.fixture(scope="session")
def file_scraper() -> StardewFileScraper:
    config_path = Path(__file__).resolve().parent / "configs" / "config_tests.json"
    config = ConfigLoader(config_path)
    return StardewFileScraper(config)


@pytest.fixture(scope="session")
def input_dir() -> Path:
    return Path(__file__).resolve().parent / "input"


def _read_html(input_dir: Path, page: str) -> str:
    path = input_dir / f"{page.strip().replace(' ', '_')}.html"
    return path.read_text(encoding="utf-8")


def test_fetch_page_reads_local_file(file_scraper: StardewFileScraper) -> None:
    html = file_scraper.fetch_page("Ice Cream")
    assert isinstance(html, str)
    assert "<html" in html.lower()
    assert len(html) > 1000


def test_parse_summary_returns_text(file_scraper: StardewFileScraper, input_dir: Path) -> None:
    html = _read_html(input_dir, "Robin")
    summary = file_scraper.parse_summary(html)

    assert isinstance(summary, str)
    assert len(summary) > 30
    print(summary)
    assert "  " not in summary


def test_extract_tables_returns_nonempty_dataframes(file_scraper: StardewFileScraper, input_dir: Path) -> None:
    html = _read_html(input_dir, "Oasis")
    tables = file_scraper.extract_tables(html)

    assert isinstance(tables, list)
    assert len(tables) >= 1
    assert isinstance(tables[0], pd.DataFrame)
    assert tables[0].shape[0] > 0


def test_fetch_page_redirections_filters_and_deduplicates(file_scraper: StardewFileScraper, input_dir: Path) -> None:
    html = _read_html(input_dir, "Ice Cream")
    links = file_scraper.fetch_page_redirections(html)

    assert isinstance(links, list)
    assert all(isinstance(x, str) for x in links)

    assert len(links) == len(set(links))

    assert all("#" not in x and "?" not in x for x in links)
    assert all(x.strip() for x in links)

    blocked_prefixes = ("File:", "Image:", "Category:", "Special:", "Help:", "Talk:", "User:", "Template:")
    assert all(not x.startswith(blocked_prefixes) for x in links)

