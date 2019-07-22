import requests
import json

DATA_URL = "https://fantasy.premierleague.com/api/bootstrap-static"
DATA_FILENAME = "data/player_data_19_20.json"

# Download all player data and write file
def get_player_data():
    r = requests.get(DATA_URL)
    jsonResponse = r.json()
    with open(DATA_FILENAME, 'w') as outfile:
        json.dump(jsonResponse, outfile)