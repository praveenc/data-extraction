# from collections import Counter
from rich import print

from unstructured.cleaners.core import (
    bytes_string_to_string,
    clean,
    clean_non_ascii_chars,
    replace_unicode_quotes,
)
from unstructured.documents.elements import ListItem, NarrativeText, Title
from unstructured.partition.pdf import partition_pdf

BASE_DIR = "./pdf"
file_name = "Retrieval_meets_Long_Context_Large_Language_Models2310.03025v1.pdf"
file_path = f"{BASE_DIR}/{file_name}"

print(f"Extracting text from {file_path}...\n")
# elements = partition_pdf(f"{BASE_DIR}/{file_name}")
elements = partition_pdf(
    file_path,
    strategy="fast",
    skip_headers_and_footers=True,
    infer_table_structure=False,
)

# print(Counter(type(element) for element in elements))
# all_text = []
# for el in elements:
#     # text = bytes_string_to_string(el.text)
#     text = el.text
#     text = clean(text)
#     text = clean_non_ascii_chars(text)
#     text = replace_unicode_quotes(text)

chunks = []
current_chunk = ""
MAX_CHUNK_SIZE = 1024

for element in elements:
    if isinstance(element, Title):
        if current_chunk:  # Flush the previous chunk
            chunks.append(current_chunk)
        current_chunk = element.text + "\n"  # Start a new chunk
    elif isinstance(element, NarrativeText):
        current_chunk += element.text + "\n"
    elif isinstance(element, ListItem):
        current_chunk += element.text + "\n"
    # Add more types here

    # Check if the current chunk is too big and needs to be split
    if len(current_chunk) >= MAX_CHUNK_SIZE:
        chunks.append(current_chunk[:MAX_CHUNK_SIZE])
        current_chunk = current_chunk[MAX_CHUNK_SIZE:]

if current_chunk:  # Don't forget the last chunk
    chunks.append(current_chunk)

print(chunks)