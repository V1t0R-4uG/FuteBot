import json
from datetime import datetime
from typing import Dict, List, Union
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup

from .utils.get_player_id_and_slug_by_team import \
    get_player_id_and_slug_by_team
from .utils.get_team_id import get_team_id
from .utils.request_and_parse_json import request_and_parse_to_object


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


def table() -> Union[List, bool]:
    """Return the current table."""
    url = (
        f'https://api.sofascore.com/api/v1/unique-tournament/325/season'
        f'/40557/standings/total'
    )
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


def team_statistics(team_name: str) -> Union[Dict, bool]:
    """Return Team Statistics."""
    TEAM_ID = get_team_id(team_name=team_name)
    url = (
        f'http://api.sofascore.com/api/v1/team/{TEAM_ID}/unique-tournament'
        f'/325/season/40557/statistics/overall'
    )
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
    url = (
        f'https://api.sofascore.com/api/v1/unique-tournament/325/season/'
        f'40557/events/round/{round_number}'
    )
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
            'time_stamp': datetime.fromtimestamp(matches['startTimestamp']),
        }
        filtered_matches_array.append(match_stats)
    return filtered_matches_array


player = Union[Dict, ValueError]


def return_player_overview(team_name: str, player_name: str) -> player:
    """Return a Dict that contains the player overview"""
    try:
        team_id = get_team_id(team_name)
        if not team_id:
            raise ValueError('O time informado não existe')
        player_information = get_player_id_and_slug_by_team(
            team_id, player_name
        )
        if player_information is None:
            raise ValueError('O jogador informado não existe!')
        player_id = player_information['player_id']
        url = f'https://api.sofascore.app/api/v1/player/{player_id}/'
        json_api_sofa = request_and_parse_to_object(url, 'GET')
        return json_api_sofa
    except ValueError as error:
        return error


def return_player_overall(team_name: str, player_name: str) -> player:
    """Returns a Dict that contains the player overall."""
    try:
        team_id = get_team_id(team_name)
        if not team_id:
            raise ValueError('O time informado não existe')
        player_info = get_player_id_and_slug_by_team(team_id, player_name)
        if player_info is None:
            raise ValueError('O jogador informado não existe')
        player_id = player_info['player_id']
        url = (
            f'http://api.sofascore.com/api/v1/player/{player_id}'\
            f'/unique-tournament/325/season/40557/statistics/overall'
        )
        json_api_sofa = request_and_parse_to_object(url, 'GET')
        return json_api_sofa
    except ValueError as error:
         return error

def return_player_photo(player_id: int) -> (str | ValueError):
    try:
        if type(player_id) != int:
            raise ValueError('O id passado é invalido')
        player_image = (
            f'https://api.sofascore.app/api/v1/player/{player_id}/image'
        )
        return player_image
    except ValueError as error:
        return error


def main() -> None:
    print(return_player_overall('atletico mineiro', 'guilherme arana'))


if __name__ == '__main__':
    main()
