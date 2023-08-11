import requests
from bs4 import BeautifulSoup
import re


def safe_response(response: requests.Response) -> dict:
    # check for 404
    if response.status_code == 200 or 201:
        resp = response.json()
        resp = resp["data"]
        return resp
    elif response.status_code == 404:
        raise Exception(f"{response.request.path_url} not found")
    else:
        print(response.status_code)
        print(response.json())
        raise Exception("broke")


def extract_human_readable_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all text elements
    text_elements = soup.find_all(text=True)

    # Combine and clean up the text
    cleaned_text = " ".join(text.strip() for text in text_elements if text.strip())

    # Remove extra whitespace and line breaks
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)

    return cleaned_text
