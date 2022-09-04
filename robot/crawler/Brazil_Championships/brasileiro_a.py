import json
from typing import Dict, List, Union
from unicodedata import normalize
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def last_results() -> Union[List, bool]:
    """Scrape the last matches results and return it in an array."""
    URL = 'https://www.soccerstats.com/latest.asp?league=brazil'
    try:
        page = requests.get(URL)
        page_content = page.text
        parsed_content = BeautifulSoup(page_content, 'html.parser')
        match_html_tag = parsed_content.find_all(
            'div', style='text-align:center;'
        )
        last_matches_results = []
        for matches in match_html_tag:
            last_matches_results.append(normalize('NFKD', matches.text))
        return last_matches_results
    except:
        return False


def request_and_parse_to_object(url: str, protocol: str = 'GET') -> Dict:
    """Request the url endpoint and return the json parsed to python object."""
    response = requests.request(protocol, url)
    response_to_object = json.loads(response.text)
    return response_to_object


def table() -> Union[List, bool]:
    """Return the current table."""
    url = 'https://api.sofascore.com/api/v1/unique-tournament/325/season\
/40557/standings/total'
    try:
        json_api_sofa = request_and_parse_to_object(url=url, protocol='GET')
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
    except:
        return False


def get_team_id(team_name: str) -> Union[str, bool]:
    """get the ID from a specific team"""
    lower_case_string = team_name.lower().replace(' ', '-')
    url = 'https://api.sofascore.com/api/v1/unique-tournament/325/season/\
40557/standings/total'
    try:
        json_api_sofa = request_and_parse_to_object(url=url, protocol='GET')
        team_list = json_api_sofa['standings'][0]['rows']
        result = [
            team['team']['id']
            for team in team_list
            if team['team']['slug'] == lower_case_string
        ]
        return result[0]
    except:
        return False


def team_statistics(team_name: str) -> Union[Dict, bool]:
    """Return Team Statistics."""
    TEAM_ID = get_team_id(team_name=team_name)
    url = f'http://api.sofascore.com/api/v1/team/{TEAM_ID}/unique-tournament\
/325/season/40557/statistics/overall'
    try:
        json_api_sofa = request_and_parse_to_object(url=url, protocol='GET')
        statistics = json_api_sofa['statistics']
        return statistics
    except:
        return False


def team_overview(team_name: str) -> Union[Dict, bool]:
    """Get the overview about an specific club."""
    TEAM_ID: Union[str, bool] = get_team_id(team_name=team_name)
    TEAM_STATS: Union[Dict, bool] = team_statistics(team_name)
    url = f'https://api.sofascore.com/api/v1/team/{TEAM_ID}'
    team_image = f'https://api.sofascore.app/api/v1/team/{TEAM_ID}/image'
    try:
        json_api_sofa = request_and_parse_to_object(url=url, protocol='GET')
        team_object = json_api_sofa['team']
        TEAM_OVERVIEW = {
            'team_fullname': team_object['fullName'],
            'stadium': team_object['venue']['stadium']['name'],
            'manager': team_object['manager']['name'],
            'city': team_object['venue']['city']['name'],
            'goalsScored': TEAM_STATS['goalsScored'],
            'goalsConceded': TEAM_STATS['goalsConceded'],
            'yellowCards': TEAM_STATS['yellowCards'],
            'redCards': TEAM_STATS['redCards'],
            'teamImage': team_image,
        }
        return TEAM_OVERVIEW
    except:
        return False


def show_matches_by_round_number(round_number: int) -> List[Dict]:
    """Show matches by round number."""
    url = f'https://api.sofascore.com/api/v1/unique-tournament/325/season/\
40557/events/round/{round_number}'
    json_api_sofa = request_and_parse_to_object(url, 'GET')
    matches_array = json_api_sofa['events']
    filtered_matches_array = []
    for matches in matches_array:
        match_stats = {
            'home_team': matches['homeTeam']['shortName'],
            'away_team': matches['awayTeam']['shortName'],
            'home_score': matches['homeScore'],
            'away_score': matches['awayScore'],
            'match_status': matches['status']['code'],
            'time_stamp': datetime.fromtimestamp(matches['startTimestamp'])
        }
        filtered_matches_array.append(match_stats)
    return filtered_matches_array


def main() -> None:
    print(show_matches_by_round_number(38))


if __name__ == '__main__':
    main()
