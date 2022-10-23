from collections import namedtuple
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup

from utils.get_player_id_and_slug_by_team import \
    get_player_id_and_slug_by_team
from utils.get_team_id import get_team_id
from utils.request_and_parse_json import request_and_parse_to_object


def last_results() -> Union[List, Dict]:
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
        return {'message': 'Erro ao tentar encontrar ultimos resultados',
                'value': False}

@dataclass(frozen=True)
class Team:
    name: str
    position: str
    matches: str
    wins: str
    losses: str
    draws: str
    scores_for: str
    points: str

def table() -> Dict:
    """Return the current table."""
    url = (
        f'https://api.sofascore.com/api/v1/unique-tournament/325/season'
        f'/40557/standings/total'
    )
    try:
        json_api_sofa = request_and_parse_to_object(url)
        table = json_api_sofa['standings'][0]['rows']
        team_array = list()
        for team in table:
            team_stats = Team(
                f"{team['team']['name']}",
                f"{team['position']}",
                f"{team['matches']}",
                f"{team['wins']}",
                f"{team['losses']}",
                f"{team['draws']}",
                f"{team['scoresFor']}",
                f"{team['points']}"
            )
            team_array.append(team_stats)
        return {'message': 'success', 'value': team_array}
    except:
        return {'message': 'Erro ao tentar trazer tabela', 'value': False}


def team_full_statistics(team_name: str) -> Dict:
    """Return Team Statistics."""
    TEAM_ID = get_team_id(team_name=team_name)
    url = (
        f'http://api.sofascore.com/api/v1/team/{TEAM_ID}/unique-tournament'
        f'/325/season/40557/statistics/overall'
    )
    try:
        json_api_sofa = request_and_parse_to_object(url)
        statistics = json_api_sofa['statistics']
        return {'message': 'success', 'value': statistics}
    except:
        return {'message': 'error', 'value': False}


@dataclass(frozen=True)
class Team_Summary:
    fullname: str
    stadium: str
    manager: str
    city: str

def team_overview(team_name: str) -> Dict:
    """Get the overview about an specific club."""
    TEAM_ID = get_team_id(team_name=team_name)
    url = f'https://api.sofascore.com/api/v1/team/{TEAM_ID}'
    try:
        json_api_sofa = request_and_parse_to_object(url)
        team_object = json_api_sofa['team']
        TEAM_OVERVIEW = Team_Summary(
            f"{team_object['fullName']}",
            f"{team_object['venue']['stadium']['name']}",
            f"{team_object['manager']['name']}",
            f"{team_object['venue']['city']['name']}"
        )
        return {'message': 'success', 'value': TEAM_OVERVIEW}
    except:
        return {'message': 'error', 'value': False}


def show_matches_by_round_number(round_number: int) -> Union[List[Tuple], Dict]:
    """Show matches by round number."""
    url = (
        f'https://api.sofascore.com/api/v1/unique-tournament/325/season/'
        f'40557/events/round/{round_number}'
    )
    try:
        json_api_sofa = request_and_parse_to_object(url, 'GET')
        matches_array = json_api_sofa['events']
        filtered_matches_array = list()
        Match = namedtuple(
            'Match',
            'home_team away_team home_score away_score match_status time_stamp'
        )
        for matches in matches_array:
            match_stats = Match(
                f"{matches['homeTeam']['shortName']}",
                f"{matches['awayTeam']['shortName']}",
                f"{matches['homeScore']}",
                f"{matches['awayScore']}",
                f"{matches['status']['code']}",
                f"{datetime.fromtimestamp(matches['startTimestamp'])}",
            )
            filtered_matches_array.append(match_stats)
        return filtered_matches_array
    except:
        return {
            'message': f'Não foi possivel trazer as informações da rodada\
            {round_number}',
            'value': False
        }




def return_player_overview(team_name: str, player_name: str) -> Dict:
    """Return a Dict that contains the player overview"""
    try:
        team_id = get_team_id(team_name)
        if not team_id:
            raise ValueError('O time informado não existe')
        player_information = get_player_id_and_slug_by_team(
            int(team_id), player_name
        )
        if player_information is None:
            raise ValueError('O jogador informado não existe!')
        player_id = player_information['player_id']
        url = f'https://api.sofascore.app/api/v1/player/{player_id}/'
        json_api_sofa = request_and_parse_to_object(url, 'GET')
        return json_api_sofa
    except ValueError as error:
        return {
            'message': error,
            'value': False
        }


def return_player_overall(team_name: str, player_name: str) -> Dict:
    """Returns a Dict that contains the player overall."""
    try:
        team_id = get_team_id(team_name)
        if not team_id:
            raise ValueError('O time informado não existe')
        player_info = get_player_id_and_slug_by_team(
            int(team_id), player_name
        )
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
        return {'message': error, 'value': False}

def return_player_photo(player_id: int) -> Union[str, Dict]:
    try:
        if type(player_id) != int:
            raise ValueError('O id passado é invalido')
        player_image = (
            f'https://api.sofascore.app/api/v1/player/{player_id}/image'
        )
        return player_image
    except ValueError as error:
        return {'message': error, 'value': False}


def main() -> None:
    team_overview('atletico mineiro')
    #table()
    #print(return_player_overall('atletico mineiro', 'guilherme arana'))


if __name__ == '__main__':
    main()
