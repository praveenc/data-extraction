from collections import Counter
from rich import print
from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean_ligatures, clean_non_ascii_chars


BASE_DIR = "./pdf"
file_name = "Retrieval_meets_Long_Context_Large_Language_Models2310.03025v1.pdf"
file_path = f"{BASE_DIR}/{file_name}"

print(f"Extracting text from {file_path}...\n")
elements = partition_pdf(file_path, strategy="fast")

print(Counter(type(element) for element in elements))

extracted_text = "\n".join([str(element.text).strip() for element in elements])

# Clean text using cleaning bricks
extracted_text = clean_ligatures(extracted_text)
extracted_text = clean_non_ascii_chars(extracted_text)
print(extracted_text)
