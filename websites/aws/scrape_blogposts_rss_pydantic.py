import os
from pathlib import Path
from typing import List
import pandas as pd
import feedparser
from bs4 import BeautifulSoup
from rich import print
import pickledb
from datetime import datetime, timezone
import json
from pydantic import BaseModel
import re


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
        return re.sub(r"<.*?>", "", text)

    def __post_init__(self):
        """Cleans the content attribute."""
        self.content = self.clean_text(self.content)


url = "https://aws.amazon.com/blogs/machine-learning/feed/"
feed = feedparser.parse(url)

# Path to store extracted blog posts to pickledb
DB_DIR = Path("db")
DB_DIR.mkdir(exist_ok=True, parents=True)

# Path to store extracted blog posts to disk
DATA_DIR = Path("data/aws/ml_blog_posts/rss")

db = pickledb.load(f"{DB_DIR}/blogposts.db", False)

processed_links = []

# Iterate over the entries in the RSS feed
for entry in feed.entries:
    link = entry.link
    filename = os.path.basename(os.path.normpath(link))
    # Check if this entry's URL is already in the pickledb
    if db.get(link):
        # This entry is already in the db, so skip it
        # print(f"Skipping: {link}")
        continue

    processed_links.append(link)

    blog_post = BlogPost(
        title=entry.title,
        tags=[tag.term for tag in entry.tags],
        authors=[author.name for author in entry.authors],
        published_date=entry.published,
        content=BeautifulSoup(entry.content[0].value, "html.parser").get_text(),
        source=link,
    )

    # Convert the blog post to a Pandas DataFrame
    df = pd.DataFrame([blog_post.dict()])

    # Save the blog post to a parquet file
    parquet_file = Path(f"{DATA_DIR}/{filename}.parquet")
    if not parquet_file.exists():
        # Save the DataFrame to a Parquet file
        # print(f"Saving: {parquet_file}")
        df.to_parquet(parquet_file, engine="pyarrow", compression="snappy")

    # # Save the blog post to the pickledb
    db.set(link, datetime.now(timezone.utc).isoformat())
    db.dump()

if len(processed_links) > 0:
    print(f"Links: {processed_links} \n saved to: {DB_DIR}/blogposts.db")
else:
    print("No new blog posts found since last run.")
