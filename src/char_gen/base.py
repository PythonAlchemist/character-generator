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
        response = requests.get(
            f"{BASE_URL}/{url}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
        )
        return safe_response(response)

    def getOrganizations(self):
        url = f"{self.base_url}/organisations"
        response = requests.get(url, headers=HEADER).json()
        data = response["data"]
        orgs = [
            {
                "name": x["name"],
                "id": x["id"],
                "members": [y["character_id"] for y in x["members"]],
            }
            for x in data
        ]
        return orgs


if __name__ == "__main__":
    kanka = Kanka()
    orgs = kanka.getOrganizations()
    print(orgs)
    # for char in orgs[0]["members"]:
    #     print(kanka.getCharacter(char))
