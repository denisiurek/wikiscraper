# wikiscraper
This project consists of a Python command-line application for scraping a Wiki of choice (in this case - Stardew Valley Wiki). This program is a basis for passing a Python course @ MIMUW


## Building and running
### Building
This project uses uv for managing dependencies.
To build the project, use `uv build` in the project root directory.

### Running
To run the project, use `uv run wikiscraper` in the project root directory.

### Usage 
To see the available options, use `uv run wikiscraper --help`.
The use of fallback google search is optional, and can be enabled by putting a free serpev.dev API key in the
.env file under the `X-API-KEY` key.

### Testing
To run the unit tests, use `uv run pytest` in the project root directory.

The integration tests can be run using `uv run python tests/integration_test.py`.

## Configuration
The configuration of the project is done through the `config.json` file.
Available options:
- `wiki_url` - the URL of the wiki to scrape
- `request_timeout` - the timeout for HTTP requests
- `user_agent` - the user agent to use for HTTP requests
- `accept-language` - the language to use for HTTP requests
- `word_freq_lang` - the language to use for word frequency analysis (wordfreq package)
- `json_path` - the path to the JSON file to save word frequencies to
- `html_path` - the path to the directory to read HTML files from (used in stardew_file mode)
- `mode` - the mode to use for scraping (see below)

Available modes:
- `stardew_normal` - scrapes the wiki normally, through the `StardewScraper` class
- `stardew_file` - scrapes the wiki using the `StardewFileScraper` class (wrapper for the `StardewScraper`), which fetches HTML files from a directory instead of fetching them online

New modes can be added by creating a new class that inherits from `WikiScraper` and implementing its abstract methods.
This allows for custom scraping logic that can be used for different wikis or different scraping strategies.



