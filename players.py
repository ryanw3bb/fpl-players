import csv
import json
import math
from get_data import get_player_data

# Constants
MAX_FDR = 5

# Data range
USE_LAST_SEASON = True
GAME_WEEK_START = 1  # GW1 = 1
GAME_WEEK_END = 6  # Inclusive

# 1 = GK, 2 = DEF, 3 = MID, 4 = ATT
POSITIONS = [1, 2, 3, 4]
EXCLUDE_TEAMS = []
MAX_VALUE = 15
MINIMUM_MINUTES_PLAYED = 500

# Price premium
COST_FACTORED = False
GK_DF_PRICE_MIN = 4
MF_FW_PRICE_MIN = 4.5


def get_estimated_points(player_data, difficulty_data):
    ppg = float(player_data['points_per_game'])
    team_id = player_data['team']
    estimated_points = 0

    for i, fdr_row in enumerate(difficulty_data):
        if i == team_id:
            data = fdr_row[0].split(',')
            for j in range(1 + GAME_WEEK_START, 2 + GAME_WEEK_END):
                match_difficulty = (MAX_FDR - float(data[j])) / (MAX_FDR / 2)
                estimated_points += ppg * match_difficulty
            break

    if COST_FACTORED:
        if player_data['element_type'] < 2:
            # GF / DF
            price_min = GK_DF_PRICE_MIN
        else:
            # MF / FW
            price_min = MF_FW_PRICE_MIN

        estimated_points = math.sqrt((estimated_points ** 2) / math.sqrt(float(player_data['now_cost']) - price_min))

    return round(estimated_points)


if USE_LAST_SEASON:
    data_file = 'data/player_data_18_19.json'
else:
    get_player_data()
    data_file = 'data/player_data_19_20.json'

print(data_file)

with open('data/gw_difficulty.csv', newline='') as csv_file, open(data_file) as json_file:
    # load match difficulty csv
    csv_data = []
    for row in csv.reader(csv_file, delimiter=' '):
        csv_data.append(row)

    # load player data json
    json_data = json.load(json_file)
    data_dict = dict()

    for element in json_data['elements']:
        if float(element['minutes']) > MINIMUM_MINUTES_PLAYED and \
                element['element_type'] in POSITIONS and \
                element['now_cost'] <= MAX_VALUE * 10:
            player_name = element['first_name'] + ' ' + element['second_name']
            data_dict[player_name] = get_estimated_points(element, csv_data)


# sort and print list
data_dict_sorted = {r: data_dict[r] for r in sorted(data_dict, key=data_dict.get)}

for attribute, value in data_dict_sorted.items():
    print(attribute, value)
