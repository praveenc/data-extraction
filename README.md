# Data Extraction

## Extracting HTML content from AWS documentation website

- Example script to scrape AWS documentation linked html pages is [scrape_linked_html.py](./websites/aws/scrape_linked_html.py)

- To upload files recursively from a local dir to S3 is available [here](./websites/aws/upload_dir_to_s3.py)

- [Scrape AWS MachineLearning Blogposts](./websites/aws/scrape_blogpost.ipynb) notebook we demonstrate how to extract content from blog posts using two methods.
  - From the websites RSS Feed (top 20 blog posts)
  - Using `BeautifulSoup` python library

    >NOTE: If you need to access more than the 20 most recent blog posts, you would need to scrape the blog directly or use a different method that doesn't rely on the RSS feed. However, please be aware that web scraping should be **done in accordance with the website's terms of service** and with respect for the server's resources.
