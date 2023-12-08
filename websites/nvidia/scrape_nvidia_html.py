import os
from argparse import ArgumentParser
from pathlib import Path

import feedparser
import requests
from rich import print

from unstructured.partition.auto import partition

BASE_DIR = Path(f"{os.getcwd()}/downloaded-html")

print(BASE_DIR)


def download_html(url: str, file_name: str) -> None:
    """
    Downloads the html content of the url to disk.
    """
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(exist_ok=True, parents=True)

    file_path = BASE_DIR.joinpath(file_name)
    content = requests.get(url).text
    file_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", help="url to download from", type=str, required=True)
    parser.add_argument(
        "--extract-text",
        help="extract text from html",
        default=True,
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--file_name",
        help="file name to save to",
        default="index.html",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--rss",
        help="download files from rss feed",
        default=False,
        action="store_true",
        required=False,
    )
    args = parser.parse_args()
    file_name = args.file_name
    if file_name == "index.html":
        # extract the file name from the url
        file_name = args.url.split("/")[-1]
        print(f"Downloading {args.url} to {file_name}")
        download_html(args.url, file_name)

    if args.extract_text:
        html_file_path = str(BASE_DIR.joinpath(file_name))
        print(f"Extracting text from {html_file_path}...")
        elements = partition(
            filename=html_file_path,
            skip_headers_and_footers=True,
            infer_table_structure=True,
        )
        text = "/n".join([element.text for element in elements])
        output_file_name = f"{file_name.split('.')[0]}.txt"
        output_file_path = BASE_DIR.joinpath(output_file_name)
        bytes_written = output_file_path.write_text(text, encoding="utf-8")

    if args.rss:
        print("Downloading rss feed")
        rss_feed_url = args.url
        feed = feedparser.parse(rss_feed_url)
        for entry in feed.entries:
            print("Entry Title:", entry.title)
            print("Entry Link:", entry.link)
            print("Entry Published Date:", entry.published)
            print("Entry Summary:", entry.summary)
            print("\n")
