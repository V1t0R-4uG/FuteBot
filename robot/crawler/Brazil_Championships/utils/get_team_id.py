from typing import Union

from .request_and_parse_json import request_and_parse_to_object


def get_team_id(team_name: str) -> Union[str, bool]:
    """get the ID from a specific team"""
    lower_case_string = team_name.lower().replace(' ', '-')
    url = (
        f'https://api.sofascore.com/api/v1/unique-tournament/325/season/'
        f'40557/standings/total'
    )
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
