from . import StardewScraper
from . import StardewFileScraper

def get_scraper_tool(config):
    if config.is_debug:
        return StardewFileScraper(config)
    return StardewScraper(config)
