import json
from typing import Dict

import requests

def request_and_parse_to_object(url: str, protocol: str = 'GET') -> Dict:
    """Request the url endpoint and return the json parsed to python object."""
    bot_session = requests.Session()
    USER_AGENT = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.126 Safari/537.36"
    }
    bot_session.headers.update(USER_AGENT)
    response = bot_session.get(url, timeout=5)
    response_to_object = json.loads(response.text)
    return response_to_object

if __name__ == "__main__":
    print(request_and_parse_to_object("https://api.sofascore.com/api/v1/tournament/83/season/40557/standings/total"))
