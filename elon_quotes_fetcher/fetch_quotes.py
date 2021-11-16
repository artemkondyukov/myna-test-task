import argparse
from tqdm import tqdm

from elon_quotes_fetcher.quote_fetcher import QuoteFetcher
from elon_quotes_fetcher.string_processor import StringProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download quotes from https://elonmusknews.org")
    parser.add_argument("--url_list", type=str,
                        help="Path to the file with urls to parse")
    parser.add_argument("--out", type=str,
                        help="Path to the file where to store parsed data")

    args = parser.parse_args()

    with open(args.url_list, "r") as f:
        elon_quotes_urls = [line.strip() for line in f.readlines()]

    result = []

    string_processor = StringProcessor()
    quote_fetcher = QuoteFetcher()

    for url in tqdm(elon_quotes_urls, total=len(elon_quotes_urls)):
        for quote in quote_fetcher.fetch_quote(url):
            current_text = string_processor.process(quote)
            result.append(current_text)

    with open(args.out, "w") as f:
        for r in result:
            f.write(r + "\n")
