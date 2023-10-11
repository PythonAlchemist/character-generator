import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
from char_gen.utils import safe_response

load_dotenv(find_dotenv())

API_KEY = os.getenv("KANKA_KEY", default=None)
CAMPAIGN_ID = os.getenv("KANKA_CAMPAIGN_ID", default=None)
HEADER = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}
BASE_URL = f"https://kanka.io/api/1.0/campaigns/{CAMPAIGN_ID}"


class Kanka:
    base_url = f"https://kanka.io/api/1.0/campaigns/{CAMPAIGN_ID}"

    assert API_KEY is not None, "API Key not found"
    assert CAMPAIGN_ID is not None, "Campaign ID not found"

    def get(url: str) -> dict:
        response = requests.get(f"{BASE_URL}/{url}", headers=HEADER)
        return safe_response(response)

    def delete(url: str) -> dict:
        response = requests.delete(f"{BASE_URL}/{url}", headers=HEADER)
        return safe_response(response)

    def post(url: str, payload: dict) -> dict:
        response = requests.post(
            f"{BASE_URL}/{url}",
            headers=HEADER,
            data=json.dumps(payload),
        )
        return safe_response(response)
