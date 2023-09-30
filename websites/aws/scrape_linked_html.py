import argparse
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Global variable to set the root directory for storing downloaded files
BASE_DIR = Path("downloaded_pages")

# Function to download HTML content from a given URL
def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to find the URL of the next topic in the HTML content
def find_next_url(soup, base_url):
    next_topic = soup.find("div", {"class": "next-link"})
    if next_topic:
        relative_url = next_topic.get("href")
        return f"{base_url}{relative_url}"
    return None

# Function to write error messages to a file
def write_error_to_file(error_message):
    with open(BASE_DIR / "errors.txt", "a") as f:
        f.write(error_message + "\n")

# Main function to handle the downloading logic
def main(start_url):
    # Create the root directory if it doesn't exist
    BASE_DIR.mkdir(exist_ok=True)

    current_url = start_url
    failed_downloads = []

    # Extract the base URL for constructing full URLs
    base_url = "/".join(start_url.split("/")[:-1]) + "/"

    while current_url:
        parsed_url = urlparse(current_url)
        file_name = parsed_url.path.split("/")[-1] or "index"
        # file_name = f"{file_name}.html"

        print(f"Downloading: {base_url}{file_name}")

        html_content = download_page(current_url)

        if html_content:
            with open(BASE_DIR / file_name, "w", encoding="utf-8") as f:
                f.write(html_content)

            soup = BeautifulSoup(html_content, "html.parser")
            next_url = find_next_url(soup, base_url)

            if next_url:
                current_url = next_url
            else:
                print("No more 'Next Topic' found. Exiting.")
                break
        else:
            failed_downloads.append(current_url)
            write_error_to_file(f"Failed to download {current_url}")

        time.sleep(1)

    if failed_downloads:
        print(f"Failed to download the following URLs: {failed_downloads}")

# Entry point of the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download HTML pages.")
    parser.add_argument(
        "--url", type=str, help="Starting URL to download from", required=True
    )
    args = parser.parse_args()
    main(args.url)
