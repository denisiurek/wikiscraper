import argparse
import sys
from time import sleep

from analysis import TextAnalyzer
from scraper import get_scraper_tool
from utils import ConfigLoader

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="WikiScraper: A tool to scrape and analyze wiki contents, specifically Stardew Valley Wiki."
    )

    # --- Primary Actions ---

    parser.add_argument(
        "--summary",
        type=str,
        help="Fetch the summary (first paragraph) of a given subpage (e.g., --summary 'Golden Walnut')."
    )

    parser.add_argument(
        "--table",
        type=str,
        help="Extract tables from a given subpage to CSV. Usage: --table 'Golden Walnut' "
             "(must be combined with --number)."
    )

    parser.add_argument(
        "--count-words",
        type=str,
        help="Count word occurrences on a subpage and append to ./word-counts.json. "
             "Usage: --count-words 'Golden Walnut'"
    )

    parser.add_argument(
        "--auto-count-words",
        type=str,
        help="Automatically follow links and count words recursively starting from this page."
    )

    parser.add_argument(
        "--analyze-relative-word-frequency",
        action="store_true",
        help="Compare word frequency against a language standard. Requires --summary or source text."
    )

    # --- Modifiers (Secondary Arguments) ---

    parser.add_argument(
        "--number",
        type=int,
        default=1,
        help="For --table: Specify which table index to extract (default: 1)."
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=['article', 'language'],
        default='language',
        help="For --analyze: Set mode to 'article' or 'language'."
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="For --analyze: Number of most common words to analyze (default: 10)."
    )

    parser.add_argument(
        "--chart",
        type=str,
        help="For --analyze: Save a plot to the specified path."
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="For --auto-count-words: Recursion depth (default: 3)."
    )

    parser.add_argument(
        "--wait",
        type=int,
        default=1,
        help="For --auto-count-words: Delay in seconds between fetches (default: 1)."
    )
    return parser

def crawl_subpages(start_subpage: str, depth: int, wait: int, scraper):
    visited, to_visit = set(), {start_subpage}
    for _ in range(depth):
        current_batch = to_visit - visited
        to_visit = set()
        for page in current_batch:
            print(f"Fetching {page}")
            html = scraper.fetch_page(page)
            words = scraper.extract_all_words(html)
            TextAnalyzer.update_word_counts_json(TextAnalyzer.sum_word_occurrences(words), "word-counts.json")
            visited.add(page)
            to_visit.update(scraper.fetch_page_redirections(html))
            sleep(wait)


def main():
    parser = setup_parser()

    config = ConfigLoader()

    args = parser.parse_args()
    scraper = get_scraper_tool(config)

    if args.summary:
        try:
            print(scraper.parse_summary(scraper.fetch_page(args.summary)))
        except Exception as e:
            print(f"Error processing summary: {e}")

    elif args.table:
        try:
            if args.number < 1:
                raise ValueError("Table number must be at least 1.")

            tables = scraper.extract_tables(scraper.fetch_page(args.table))

            if args.number > len(tables):
                raise ValueError("Table number exceeds number of tables.")

            table = tables[args.number - 1]
            table.to_csv(f"{args.table}_{args.number}.csv")

            print(f"Table saved to {args.table}_{args.number}.csv")

            print(TextAnalyzer.sum_word_occurrences(table))

        except Exception as e:
            print(f"Error processing table: {e}")



    elif args.count_words:
        try:
            words = scraper.extract_all_words(scraper.fetch_page(args.count_words))
            word_counts = TextAnalyzer.sum_word_occurrences(words)
            TextAnalyzer.update_word_counts_json(word_counts, "word-counts.json")
            print(f"Word counts updated in word-counts.json")

        except Exception as e:
            print(f"Error counting words: {e}")

    elif args.analyze_relative_word_frequency:
        try:
            df = TextAnalyzer.analyze_rel_word_freq(args.mode, args.count, config.word_freq_lang, config.json_path)
            print(df)
            if args.chart: TextAnalyzer.plot_rel_word_freq(df, args.chart)

        except Exception as e:
            print(f"Error in analysis: {e}")


    elif args.auto_count_words:
        try:
            crawl_subpages(args.auto_count_words, args.depth, args.wait, scraper)
        except Exception as e:
            print(f"Error in auto word counting: {e}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
