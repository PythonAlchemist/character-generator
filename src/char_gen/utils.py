import requests
from bs4 import BeautifulSoup
import re
import tiktoken


def safe_response(response: requests.Response) -> dict:
    # check for 404
    if response.status_code == 200 or 201:
        resp = response.json()
        resp = resp["data"]
        return resp
    elif response.status_code == 204:
        return {}
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


def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
