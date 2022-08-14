import json
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


def table():
    """Scrape the current table"""
    url = 'https://api.sofascore.com/api/v1/unique-tournament/325/season/40557/standings/total'
    response = requests.request('GET', url)
    json_api_sofa = json.loads(response.text)
    table = json_api_sofa['standings'][0]['rows']
    team_array = []
    for team in table:
        team_stats = {
            'team_name': team['team']['name'],
            'team_position': team['position'],
            'team_matches': team['matches'],
            'team_wins': team['wins'],
            'team_losses': team['losses'],
            'team_draws': team['draws'],
            'team_scores_for': team['scoresFor'],
            'team_points': team['points'],
        }
        team_array.append(team_stats)
    return team_array
