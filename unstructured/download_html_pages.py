import scrape_linked_html
from tqdm import tqdm

urls = [
    "https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html",
    "https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html",
    "https://docs.aws.amazon.com/sagemaker/latest/dg/mlops.html",
    "https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers.html",
    "https://docs.aws.amazon.com/sagemaker/latest/dg/model-explainability.html",
    "https://docs.aws.amazon.com/sagemaker/latest/dg/governance.html",
    "https://docs.aws.amazon.com/sagemaker/latest/dg/security.html",
]

for url in tqdm(urls, total=len(urls), desc="Downloading HTML pages"):
    scrape_linked_html.main(url)
