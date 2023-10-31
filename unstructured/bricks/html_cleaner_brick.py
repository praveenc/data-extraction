from rich import print

from unstructured.cleaners.core import (
    bytes_string_to_string,
    clean,
    clean_non_ascii_chars,
    replace_unicode_quotes,
)
from unstructured.documents.elements import ListItem, NarrativeText, Table, Title

# from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html
from unstructured.staging.base import convert_to_dict, elements_to_json

# from unstructured.partition.html import partition_html
# from unstructured.staging.base import convert_to_dict

# url = "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"
# with open("../example-docs/example-10k.html", "rb") as f:
with open("../html/aws_cost_management/what-is-costmanagement.html", "rb") as f:
    elements = partition_html(
        file=f, skip_headers_and_footers=True, infer_table_structure=True
    )


def clean_text(text):
    text = replace_unicode_quotes(text)
    text = bytes_string_to_string(text)
    text = clean_non_ascii_chars(text)
    text = clean(
        text,
        bullets=True,
        extra_whitespace=True,
        trailing_punctuation=True,
        lowercase=True,
        dashes=True,
    )
    return text


# Gather only text elements and clean them
text_elements = [
    clean_text(el.text)
    for el in elements
    if (
        isinstance(el, NarrativeText)
        # or isinstance(el, Title)
        or isinstance(el, Table)
        or isinstance(el, ListItem)
    )
]

print(text_elements)
