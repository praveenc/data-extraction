from collections import Counter

from rich import print

from unstructured.documents.elements import NarrativeText, Table, Title
from unstructured.partition.auto import partition
from unstructured.staging.base import convert_to_dict, elements_to_json

# from unstructured.partition.html import partition_html
# from unstructured.staging.base import convert_to_dict

# url = "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"
# with open("../example-docs/example-10k.html", "rb") as f:
with open("../html/aws_cost_management/what-is-costmanagement.html", "rb") as f:
    elements = partition(
        file=f, skip_headers_and_footers=True, infer_table_structure=True
    )

filename = "output.dict"
element_dict = convert_to_dict(elements)

# json_filename = "output.json"
# elements_to_json(elements, json_filename)

# print(type(element_dict))
print(len(element_dict))

for txt_dict in element_dict:
    if txt_dict["type"] in ["Title", "NarrativeText", "Table"]:
        print(txt_dict["text"])
