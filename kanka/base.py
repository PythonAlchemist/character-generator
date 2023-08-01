import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
from utils import safe_response

load_dotenv(find_dotenv())

API_KEY = os.getenv("KANKA_KEY", default=None)
CAMPAIGN_ID = os.getenv("KANKA_CAMPAIGN_ID", default=None)


class Kanka:
    def __init__(self, api_key: str = API_KEY, campaign_id: int = CAMPAIGN_ID):
        self.api_key = api_key
        self.campaign_id = campaign_id
        self.base_url = f"https://kanka.io/api/1.0/campaigns/{campaign_id}"
        self.header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        assert api_key is not None, "API Key not found"
        assert campaign_id is not None, "Campaign ID not found"

    def getCharacter(self, id: int) -> dict:
        url = f"{self.base_url}/characters/{id}"
        response = safe_response(requests.get(url, headers=self.header))

        return response

    def getOrganizations(self):
        url = f"{self.base_url}/organisations"
        response = requests.get(url, headers=self.header).json()
        data = response["data"]
        orgs = [
            {
                "name": x["name"],
                "id": x["id"],
                "members": [y["id"] for y in x["members"]],
            }
            for x in data
        ]
        return orgs


if __name__ == "__main__":
    kanka = Kanka()
    orgs = kanka.getOrganizations()
    for char in orgs[0]["members"]:
        print(kanka.getCharacter(char))
