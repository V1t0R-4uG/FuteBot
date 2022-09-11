from typing import Dict

from .request_and_parse_json import request_and_parse_to_object


def get_player_id_and_slug_by_team(team_id: int, player_name: str) -> Dict:
    """Return an object that contains the slug and the id of the player."""
    player_formated_name = player_name.lower().replace(' ', '-')
    url = f'https://api.sofascore.com/api/v1/team/{team_id}/players'
    json_api_sofa = request_and_parse_to_object(url, 'GET')
    players = json_api_sofa['players']
    for player in players:
        player_slug = player['player']['slug']
        if player_slug != player_formated_name:
            continue
        player_info = {
            'player_slug': player_slug,
            'player_id': player['player']['id'],
        }
        return player_info
