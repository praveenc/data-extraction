from rich import print

from unstructured.chunking.title import chunk_by_title
from unstructured.documents.elements import Title
from unstructured.partition.html import partition_html

# url = "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"
with open("../html/aws_cost_management/what-is-costmanagement.html", "rb") as f:
    elements = partition_html(
        file=f, skip_headers_and_footers=True, infer_table_structure=True
    )

# Get only interested elements
# elements_of_interest = [el.text for el in elements if isinstance(el, Title)]

# replace the following text with nothing
txt_to_replace = [
    "Getting started",
    "Did this page help you? - Yes",
    "Did this page help you? - No",
    "Thanks for letting us know we're doing a good job!",
    "If you've got a moment, please tell us what we did right so we can do more of it.",
    "Thanks for letting us know this page needs work. We're sorry we let you down.",
    "If you've got a moment, please tell us how we can make the documentation better.",
]

# Thanks for letting us know we're doing a good job!
# If you've got a moment, please tell us what we did right so we can do more of it.

chunks = chunk_by_title(elements)

for chunk in chunks:
    for tr in txt_to_replace:
        chunk.text = chunk.text.replace(tr, "")
    if len(chunk.text) > 0:
        print(chunk)
    print("\n\n" + "-" * 80)
