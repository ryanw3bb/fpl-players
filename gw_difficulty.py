import csv

GAME_WEEK_START = 1
GAME_WEEK_END = 6

with open('data/gw_difficulty_19_20.csv', newline='') as csv_file:
    csv_data = []
    for row in csv.reader(csv_file, delimiter=' '):
        csv_data.append(row)

    del csv_data[0]

    data_dict = dict()

    for i, row in enumerate(csv_data):
        data = row[0].split(',')
        match_difficulty = 0
        for j in range(1 + GAME_WEEK_START, 2 + GAME_WEEK_END):
            match_difficulty += float(data[j])

        data_dict[data[0]] = round(match_difficulty)

data_dict_sorted = {r: data_dict[r] for r in sorted(data_dict, key=data_dict.get)}

for attribute, value in data_dict_sorted.items():
    print(attribute, value)