import csv
import json

class Opponent:
  away = []
  home = []

opponent_map = {
    1: 1,
    2: 16,
    3: 2,
    4: 3,
    5: 4,
    6: 6,
    7: 7,
    8: 8,
    9: 11,
    10: 12,
    11: 13,
    12: 14,
    13: 15,
    14: 4,
    15: 5,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20
}

# Data
HISTORICAL_DATA = 'data/player_gw_data_18_19.csv'
PLAYER_DATA = 'data/player_data_18_19.json'
GAMEWEEK_DATA = 'data/gw_fixtures_19_20.csv'

# Range
GAME_WEEK_START = 3  # GW1 = 1
GAME_WEEK_END = 6  # Inclusive

# 1 = GK, 2 = DEF, 3 = MID, 4 = ATT
POSITIONS = [1, 2, 3, 4]
EXCLUDE_TEAMS = []
MAX_VALUE = 15
MIN_MINUTES_PLAYED = 500


def get_opponents(p_data, f_data):
    team_id = p_data['team']
    opponents = []
    for r in f_data[1:]:
        data = r[0].split(',')
        if int(data[1]) == int(team_id):
            for i in range(3 + GAME_WEEK_START, 4 + GAME_WEEK_END):
                opponents.append(opponent_map[int(data[i])])
            break

    return opponents


def get_last_season_points(p_name, opponent_list, game_data):
    points = 0
    for r in game_data[1:]:
        data = r[0].split(',')
        if str(p_name) in str(data[0]):
            if int(data[31]) in opponent_list:
                points += float(data[47]) / 2  # home and away

    return points


with open(GAMEWEEK_DATA, newline='\n') as csv_file, open(PLAYER_DATA) as json_file:
    # load fixture csv
    fixture_data = []
    for row in csv.reader(csv_file, delimiter='\n'):
        fixture_data.append(row)

    # load player data json
    player_data = json.load(json_file)
    fixture_dict = dict()
    points_dict = dict()

    for element in player_data['elements']:
        if float(element['minutes']) > MIN_MINUTES_PLAYED and \
                element['element_type'] in POSITIONS and \
                element['now_cost'] <= MAX_VALUE * 10 and \
                element['team'] not in EXCLUDE_TEAMS:
            player_name = element['first_name'] + '_' + element['second_name']
            fixture_dict[player_name] = get_opponents(element, fixture_data)

    for attribute, value in fixture_dict.items():
        print(attribute, value)

    with open(HISTORICAL_DATA, newline='\n') as raw_file:
        # load match difficulty csv
        gw_data = []
        for row in csv.reader(raw_file, delimiter='\n'):
            gw_data.append(row)

        for attribute, value in fixture_dict.items():
            points_dict[attribute] = get_last_season_points(attribute, value, gw_data)

    # sort and print list
    data_dict_sorted = {r: points_dict[r] for r in sorted(points_dict, key=points_dict.get)}

    for attribute, value in data_dict_sorted.items():
        print(attribute, value)
