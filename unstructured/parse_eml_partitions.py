from collections import Counter

from rich import print

# from unstructured.cleaners.core import group_broken_paragraphs
from unstructured.documents.html import HTMLNarrativeText, HTMLTable, HTMLTitle
from unstructured.partition.auto import partition

BASE_DIR = "./data/eml"

file_name = "Last week on the AWS Machine Learning Blog | May 15 - 21, 2022.eml"
file_path = f"{BASE_DIR}/{file_name}"

titles_to_ignore = set(["Twitter |", "LinkedIn |", "Facebook"])


elements = partition(
    filename=file_path, skip_headers_and_footers=True, infer_table_structure=True
)

print(Counter(type(element) for element in elements))
text = []
for element in elements:
    if element.text not in titles_to_ignore:
        text.append(element.text.strip())
        # print("\n")

print("\n".join(text))
# narr_text = "\n".join(
#     [element.text for element in elements if isinstance(element, HTMLNarrativeText)]
# )

# print(title_text)
# print(" ==== Narrative text ==== ")
# print(narr_text)
