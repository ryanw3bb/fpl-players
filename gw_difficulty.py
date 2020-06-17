import json
from get_data import get_player_data, get_fixtures_data

GAME_WEEK_START = 39
GAME_WEEK_END = 39

data_file = get_player_data()
fixtures_file = get_fixtures_data()

with open(fixtures_file) as fixtures, open(data_file) as data:

    # get fixture difficulties for each team id
    fixtures_data = json.load(fixtures)
    data_dict = dict()

    for event in fixtures_data:
        if GAME_WEEK_START <= event['event'] <= GAME_WEEK_END:
            if event['team_h'] in data_dict:
                data_dict[event['team_h']] += event['team_h_difficulty']
            else:
                data_dict[event['team_h']] = event['team_h_difficulty']

            if event['team_a'] in data_dict:
                data_dict[event['team_a']] += event['team_a_difficulty']
            else:
                data_dict[event['team_a']] = event['team_a_difficulty']

    # convert team ids to names
    json_data = json.load(data)
    team_dict = dict()

    for team_id, difficulty in data_dict.items():
        for team in json_data['teams']:
            if team['id'] == team_id:
                team_dict[team['name']] = difficulty
                continue

# sort by difficulty
team_dict_sorted = {r: team_dict[r] for r in sorted(team_dict, key=team_dict.get)}

for attribute, value in team_dict_sorted.items():
    print(attribute, value)