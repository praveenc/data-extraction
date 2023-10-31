import os
import time
from urllib.parse import urlparse

import boto3
import requests
from bs4 import BeautifulSoup

# Initialize S3 client
s3 = boto3.client("s3")

# Get environment variable for S3 bucket
S3_BUCKET = os.environ["S3_BUCKET"]


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


# Function to write HTML content to S3
def write_to_s3(file_name, content):
    s3.put_object(Body=content, Bucket=S3_BUCKET, Key=file_name)


# Lambda function handler
def lambda_handler(event, context):
    # Get the URL from the event object
    start_url = event.get("url", "")
    if not start_url:
        return {"statusCode": 400, "body": "URL not provided."}

    current_url = start_url
    failed_downloads = []

    # Extract the base URL for constructing full URLs
    base_url = "/".join(start_url.split("/")[:-1]) + "/"

    while current_url:
        parsed_url = urlparse(current_url)
        file_name = parsed_url.path.split("/")[-1] or "index"
        file_name = f"{file_name}.html"

        print(f"Downloading: {base_url}{file_name}")

        html_content = download_page(current_url)

        if html_content:
            write_to_s3(file_name, html_content)

            soup = BeautifulSoup(html_content, "html.parser")
            next_url = find_next_url(soup, base_url)

            if next_url:
                current_url = next_url
            else:
                print("No more 'Next Topic' found. Exiting.")
                break
        else:
            failed_downloads.append(current_url)
            print(f"Failed to download {current_url}")

        time.sleep(1)

    if failed_downloads:
        print(f"Failed to download the following URLs: {failed_downloads}")

    return {"statusCode": 200, "body": "Scraping completed."}
