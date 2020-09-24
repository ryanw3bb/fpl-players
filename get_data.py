"""
Retrieves data as json files from fantasy.premierleague.com
"""

import json
import requests

LAST_SEASON_DATA_FILENAME = "data/player_data_19_20.json"

DATA_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
DATA_FILENAME = "data/player_data_20_21.json"

FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"
FIXTURES_FILENAME = "data/fixtures_data_20_21.json"


# Download all player data and write file
def get_player_data(use_last_season):

    if use_last_season:
        return LAST_SEASON_DATA_FILENAME

    r = requests.get(DATA_URL)
    json_response = r.json()
    with open(DATA_FILENAME, 'w') as out_file:
        json.dump(json_response, out_file)

    return DATA_FILENAME


# Download all fixtures data and write file
def get_fixtures_data():
    r = requests.get(FIXTURES_URL)
    json_response = r.json()
    with open(FIXTURES_FILENAME, 'w') as out_file:
        json.dump(json_response, out_file)

    return FIXTURES_FILENAME
