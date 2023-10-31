from datetime import datetime

from rich import print

from unstructured.cleaners.core import (
    bytes_string_to_string,
    clean,
    clean_non_ascii_chars,
    replace_unicode_quotes,
)
from unstructured.cleaners.extract import (
    extract_datetimetz,
    extract_email_address,
    extract_ip_address_name,
    extract_us_phone_number,
)
from unstructured.documents.elements import ListItem, NarrativeText, Table, Title

# from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html

# url = "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"
# with open("../example-docs/example-10k.html", "rb") as f:
with open("../html/aws_cost_management/what-is-costmanagement.html", "rb") as f:
    elements = partition_html(
        file=f, skip_headers_and_footers=True, infer_table_structure=True
    )


def replace_pii_from_text(text):
    ip_addresses = extract_ip_address_name(text)
    email_addresses = extract_email_address(text)
    us_phone_numbers = extract_us_phone_number(text)
    datetimetz = extract_datetimetz(text)

    # Replace PII from text
    text = (
        text
        if len(ip_addresses) == 0
        else [text.replace(ip_addr, "IP_ADDR") for ip_addr in ip_addresses][-1]
    )

    if len(ip_addresses) > 0:
        for ip_addr in ip_addresses:
            text = text.replace(ip_addr, "IP_ADDR")
    if len(email_addresses) > 0:
        for email_addr in email_addresses:
            text = text.replace(email_addr, "EMAIL_ADDR")
    if len(us_phone_numbers) > 0:
        for us_phone_number in us_phone_numbers:
            text = text.replace(us_phone_number, "US_PHONE_NUMBER")
    # if isinstance(datetimetz, datetime):
    #     datetimetz_str = datetimetz.strftime("%Y-%m-%d %H:%M:%S")

    #     text = text.replace(datetimetz_str, "DATETIME")
    return text


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

# Replace PII from text elements
text_elements = [replace_pii_from_text(text) for text in text_elements]

print(text_elements)
