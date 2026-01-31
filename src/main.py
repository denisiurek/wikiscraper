import argparse
import sys

from scraper import StardewScraper
from scraper import get_scraper_tool
from analysis import TextAnalyzer
from utils import ConfigLoader

#from scraper.stardew import StardewScraper
#from analysis.text_analyzer import TextAnalyzer



def main():
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
        nargs='?',
        const="./chart.png",
        help="For --analyze: Save a plot to the specified path (default: ./chart.png)."
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

            print(TextAnalyzer.sum_word_occurences(table))

        except Exception as e:
            print(f"Error processing table: {e}")



    elif args.count_words:
        try:
            raise NotImplementedError("counting not implemented")

        except Exception as e:
            print(f"Error counting words: {e}")

    elif args.analyze_relative_word_frequency:
        try:
            raise NotImplementedError("analysis not implemented")

        except Exception as e:
            print(f"Error in analysis: {e}")


    elif args.auto_count_words:
        try:
            raise NotImplementedError("autocount not implemented")

        except Exception as e:
            print(f"Error in auto word counting: {e}")

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()