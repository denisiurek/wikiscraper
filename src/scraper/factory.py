def get_scraper_tool(config):
    if config.is_debug:
        from .stardew_file_wrapper import StardewFileScraper
        return StardewFileScraper(config)
    else:
        from .stardew import StardewScraper
        return StardewScraper(config)
