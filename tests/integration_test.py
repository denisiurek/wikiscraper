import sys
import argparse
from pathlib import Path
from wikiscraper import StardewFileScraper, ConfigLoader


def run_integration_test(test_phrase, expected_start):
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "input"

    if not input_dir.exists():
        print(f"ERROR: Input directory not found at {input_dir}")
        sys.exit(1)


    print(f"Running integration test")
    print(f"Source Directory: {input_dir}")
    print(f"Target Phrase:'{test_phrase}'")

    try:
        config_path = Path(__file__).resolve().parent / "configs" / "config_tests.json"
        config = ConfigLoader(config_path)

        scraper = StardewFileScraper(config)

        html_content = scraper.fetch_page(test_phrase)
        summary = scraper.parse_summary(html_content)

        print(f"\nExtracted Summary:\n{summary}\n")

        if not summary:
            raise AssertionError("Summary is empty.")

        if expected_start not in summary:
            raise AssertionError(f"Summary does not contain expected start phrase: '{expected_start}'")

        forbidden_substrings = ["<p>", "</div>", "<b>", "href="]
        for bad_string in forbidden_substrings:
            if bad_string in summary:
                raise AssertionError(f"Summary contains unparsed HTML: '{bad_string}'")

        print("SUCCESS: Integration test passed.")
        sys.exit(0)

    except FileNotFoundError:
        print(f"FAILURE: Could not find HTML file for phrase '{test_phrase}' in {input_dir}")
        print(f"Ensure '{test_phrase.replace(' ', '_')}.html' exists.")
        sys.exit(1)
    except AssertionError as e:
        print(f"FAILURE: Assertion failed - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAILURE: An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run integration tests for WikiScraper.")
    parser.add_argument("phrase", nargs="?", default="Golden Walnut",
                        help="The phrase/filename to test (default: Golden Walnut)")
    parser.add_argument("expected", nargs="?", default="Golden Walnuts are the currency of the parrots on Ginger Island.",
                        help="Text expected to appear in the summary")

    args = parser.parse_args()

    run_integration_test(args.phrase, args.expected)