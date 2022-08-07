from unicodedata import normalize

import requests
from bs4 import BeautifulSoup


def last_results():
    """Scrape the last matches results and return it in an array."""
    URL = 'https://www.soccerstats.com/latest.asp?league=brazil'
    page = requests.get(URL)
    page_content = page.text
    parsed_content = BeautifulSoup(page_content, 'html.parser')
    match_html_tag = parsed_content.find_all('div', style='text-align:center;')
    last_matches_results = []
    for matches in match_html_tag:
        last_matches_results.append(normalize('NFKD', matches.text))
    return last_matches_results
