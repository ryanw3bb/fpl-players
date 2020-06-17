import json
from get_data import get_player_data, get_fixtures_data

# Data range
GAME_WEEK_START = 39  # GW1 = 1
GAME_WEEK_END = 39  # Inclusive

# 1 = GK, 2 = DEF, 3 = MID, 4 = ATT
POSITIONS = [1, 2, 3, 4]
EXCLUDE_TEAMS = []
MAX_VALUE = 15
MIN_MINUTES_PLAYED = 1000


def get_estimated_points(player_data, fixtures_data):
    ppg = float(player_data['points_per_game'])
    team_id = player_data['team']
    estimated_points = 0

    for event in fixtures_data:
        if GAME_WEEK_START <= event['event'] <= GAME_WEEK_END:
            if event['team_h'] == team_id:
                match_difficulty = event['team_a_difficulty'] / event['team_h_difficulty']
                estimated_points += ppg * match_difficulty
            elif event['team_a'] == team_id:
                match_difficulty = event['team_h_difficulty'] / event['team_a_difficulty']
                estimated_points += ppg * match_difficulty

    return round(estimated_points)


data_file = get_player_data()
fixtures_file = get_fixtures_data()

with open(fixtures_file) as fixtures, open(data_file) as data:

    # load fixtures data
    fixture_data = json.load(fixtures)

    # load player data
    json_data = json.load(data)
    data_dict = dict()

    for element in json_data['elements']:
        if float(element['minutes']) > MIN_MINUTES_PLAYED and \
                element['element_type'] in POSITIONS and \
                element['now_cost'] <= MAX_VALUE * 10 and \
                element['team'] not in EXCLUDE_TEAMS:
            player_name = element['first_name'] + ' ' + element['second_name']
            data_dict[player_name] = get_estimated_points(element, fixture_data)


# sort and print list
data_dict_sorted = {r: data_dict[r] for r in sorted(data_dict, key=data_dict.get)}

for attribute, value in data_dict_sorted.items():
    print(attribute, value)
