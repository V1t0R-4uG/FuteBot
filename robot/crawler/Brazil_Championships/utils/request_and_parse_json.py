import json
from typing import Dict

import requests


def request_and_parse_to_object(url: str, protocol: str = 'GET') -> Dict:
    """Request the url endpoint and return the json parsed to python object."""
    response = requests.request(protocol, url)
    response_to_object = json.loads(response.text)
    return response_to_object
