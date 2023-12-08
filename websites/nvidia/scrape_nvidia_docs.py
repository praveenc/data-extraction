import bs4
import requests


# function to extract all text under a div with a class name
def extract_text(url: str, div_class_name: str):
    # use bs4 to extract the text from the url and then by div_class_name
    response = requests.get(url)
    html_content = response.text
    # extract all text under the div with the class name
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    title = soup.title.text.strip()
    div = soup.find("div", {"class": div_class_name})
    # return the text inside the tag element
    if div:
        return div.text.strip()
