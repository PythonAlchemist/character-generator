import requests


def safe_response(response: requests.Response) -> dict:
    # check for 404
    if response.status_code == 200:
        resp = response.json()
        resp = resp["data"]
        return resp
    elif response.status_code == 404:
        raise Exception(f"{response.request.path_url} not found")
    else:
        raise Exception("broke")
