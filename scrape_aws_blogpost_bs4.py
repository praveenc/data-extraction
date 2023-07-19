import os
import json
import re

import requests
import pickledb

from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from rich import print
from datetime import datetime, timezone
from pydantic import BaseModel
from argparse import ArgumentParser


# Path to store extracted blog posts to
DATADIR = Path("./data/blog_posts")
DATADIR.mkdir(parents=True, exist_ok=True)


# Path to store extracted blog posts to pickledb
DB_DIR = Path("db")
DB_DIR.mkdir(exist_ok=True, parents=True)


class BlogPost(BaseModel):
    title: str
    tags: List[str]
    authors: List[str]
    published_date: str
    content: str
    source: str

    @staticmethod
    def clean_text(text: str) -> str:
        """Cleans the text of HTML tags and other special characters."""
        text = re.sub(r"\n\s*\n", "\n\n", text)  # Remove consecutive blank lines
        text = re.sub(
            r"\s+", " ", text
        )  # Replace multiple white spaces with a single space
        return text

    def __post_init__(self):
        """Cleans the content attribute."""
        self.content = self.clean_text(self.content)


# function to get the content of a single blog post using BeautifulSoup
def scrape_aws_blogpost(url: str, db: pickledb.PickleDB) -> str:
    """Scrapes a single blog post from AWS."""
    # Get the blog post's HTML
    post_name = url.split("/")[-2]
    json_file = Path(f"{DATADIR}/{post_name}.json")

    if db.get(url):
        # This entry is already in the db, so skip it
        print(f"Skipping {url}")
        json_file  = ""

    else:
        if not json_file.exists():
            print(f"Scraping {url}")

            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Locate and extract the desired information
                title = soup.find("h1", class_="blog-post-title").text.strip()
                # metadata = soup.find('footer', class_='blog-post-meta').text.strip()
                tag_elements = soup.find_all(
                    "span", attrs={"property": "articleSection"}
                )
                tags = [tag_element.text for tag_element in tag_elements]
                # print(metadata)

                author_elements = soup.find_all("span", attrs={"property": "author"})
                # Extract the author names and store them in a list
                author_names = [
                    author_element.find("span", attrs={"property": "name"}).text
                    for author_element in author_elements
                ]
                # print(author_names)

                # Extract datePublished
                time_element = soup.find("time", attrs={"property": "datePublished"})
                date_published = time_element["datetime"]
                # print(date_published)

                section_element = soup.find("section", class_="blog-post-content")
                content = section_element.text.strip()

                blog_post = BlogPost(
                    title=title,
                    tags=tags,
                    authors=author_names,
                    published_date=date_published,
                    content=content,
                    source=url,
                )

                # Store the blog post as json file
                with open(f"{DATADIR}/{post_name}.json", "w") as f:
                    json.dump(blog_post.dict(), f)

                # Store the blog post in the pickledb
                db.set(url, datetime.now(timezone.utc).isoformat())
                db.dump()

    return json_file


# main function to call the scrape_aws_blogpost function for each blog post
if __name__ == "__main__":
    # accept the url as an argument
    parser = ArgumentParser()
    parser.add_argument("url", type=str)
    args = parser.parse_args()

    # initialize pickledb
    db = pickledb.load(f"{DB_DIR}/blogposts.db", False)

    # Replace with the URL of the blog post you want to scrape
    urls = [
        args.url,
    ]

    for url in urls:
        scraped_post = scrape_aws_blogpost(url, db)
        if len(scraped_post) == 0:
            print(f"Skippeed writing Post.")
        else:
            print(f"Post written to {scraped_post}")
