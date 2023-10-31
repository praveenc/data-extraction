from rich import print
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

from unstructured.documents.elements import ListItem, NarrativeText, Table, Title

# from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html
from unstructured.staging.base import convert_to_dict
from unstructured.staging.huggingface import (
    chunk_by_attention_window,
    stage_for_transformers,
)

# url = "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"
# with open("../example-docs/example-10k.html", "rb") as f:
with open("../html/aws_cost_management/what-is-costmanagement.html", "rb") as f:
    elements = partition_html(
        file=f, skip_headers_and_footers=True, infer_table_structure=True
    )


# Get only interested elements
elements_of_interest = [
    el.text
    for el in elements
    if (
        isinstance(el, NarrativeText)
        # or isinstance(el, Title)
        # or isinstance(el, Table)
        # or isinstance(el, ListItem)
    )
]

# elements_dict = convert_to_dict(elements_of_interest)
# print(elements_dict)
# print(elements_of_interest)

print("Staging for Transformers")
model_name = "thenlper/gte-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

model_max_length = tokenizer.model_max_length

chunks = stage_for_transformers(
    elements_of_interest,
    tokenizer,
    model_max_length=model_max_length,
    chunk_separator="\n",
)

# text = " ".join(elements_of_interest)
# chunks = chunk_by_attention_window(text, tokenizer)

results = [nlp(chunk) for chunk in chunks]

print(results)
