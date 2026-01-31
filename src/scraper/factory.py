from . import StardewScraper
from . import StardewFileScraper

def get_scraper_tool(config):
    if config.get("is_debug"):
        return StardewFileScraper(config)
    return StardewScraper(config)
