from collections import Counter
from rich import print
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import clean_ligatures, clean_non_ascii_chars
import re

BASE_DIR = "../data/html"
file_name = "inference-pipelines.html"
file_path = f"{BASE_DIR}/{file_name}"

elements = partition_html(
    filename=file_path, chunking_strategy="by_title", skip_header_and_footers=True
)

print(Counter(type(element) for element in elements))

extracted_text = "\n".join([element.text for element in elements])

# Remove common text that appears at the beginning of a page
pattern1 = r"^AWS.*?Developer Guide"
extracted_text = re.sub(pattern1, "", extracted_text, flags=re.DOTALL)
# Remove junk text from end of page
pattern2 = r"Javascript is disabled.*?make the documentation better\."
extracted_text = re.sub(pattern2, "", extracted_text, flags=re.DOTALL)

# Clean text using cleaning bricks
extracted_text = clean_ligatures(extracted_text)
extracted_text = clean_non_ascii_chars(extracted_text)


# Extracting link_urls from element's metadata
extracted_urls = []
for element in elements:
    urls = element.metadata.link_urls
    if urls is not None:
        extracted_urls.extend(urls)

print(f"Extracted: URLs:\n{extracted_urls}")
print(f"Extracted Text: {extracted_text}")
