import pandas as pd
import os, sys
import pdb
from difflib import SequenceMatcher

RELATIVE_COL = [
    "G",
    "GS",
    "MP",
    "FG",
    "FGA",
    "3P",
    "3PA",
    "2P",
    "2PA",
    "FT",
    "FTA",
    "ORB",
    "DRB",
    "TRB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PF",
    "PTS",
    "PER",
    "OWS",
    "DWS",
    "WS",
    "WS/48",
    "OBPM",
    "DBPM",
    "BPM",
    "VORP",
]

ABSOLUTE_COL = [
    "FG%",
    "3P%",
    "2P%",
    "eFG%",
    "FT%",
    "TS%",
    "3PAr",
    "FTr",
    "ORB%",
    "DRB%",
    "TRB%",
    "AST%",
    "STL%",
    "BLK%",
    "TOV%",
    "USG%",
]

GROUP_DICT = {
    "Shooting": [
        "FG",
        "FGA",
        "3P",
        "3PA",
        "2P",
        "2PA",
        "FT",
        "FTA",
        "PTS",
        "FG%",
        "3P%",
        "2P%",
        "eFG%",
        "FT%",
        "TS%",
        "3PAr",
        "FTr",
    ],
    "Defense": [
        "STL",
        "BLK",
        "DWS",
        "DBPM",
        "STL%",
        "BLK%",
    ],
    "Rebounding": [
        "ORB",
        "DRB",
        "TRB",
        "ORB%",
        "DRB%",
        "TRB%",
    ],
    "Playmaking": [
        "AST",
        "TOV",
        "AST%",
        "TOV%",
        "USG%",
    ],
    "Miscellaneous": [
        "G",
        "GS",
        "MP",
        "PF",
        "PER",
        "OWS",
        "WS",
        "WS/48",
        "OBPM",
        "BPM",
        "VORP",
    ],
}


def make_dataset(path, offset=4):
    directory = os.listdir(path)
    list_of_df = []
    for file in directory:
        y = path + "/" + file
        df_player = pd.read_csv(y)
        df_player.insert(0, "Name", (file[: len(file) - offset]))
        list_of_df.append(df_player)
    df_main = pd.concat(list_of_df)
    return df_main


def absolute_comparison(player1_stat, player2_stat):
    return player2_stat - player1_stat


def relative_comparison(player1_stat, player2_stat):
    return ((player2_stat - player1_stat) / player1_stat) * 100


def stat_checker(df, player1_name, player1_year, player2_name, player2_year):
    df_player1 = df[(df.Name == player1_name) & (df.Season == player1_year)]
    df_player1.drop(["Name", "Season", "Age", "Tm", "Lg", "Pos"], axis=1, inplace=True)
    df_player2 = df[(df.Name == player2_name) & (df.Season == player2_year)]
    df_player2.drop(["Name", "Season", "Age", "Tm", "Lg", "Pos"], axis=1, inplace=True)
    stats_comparison_dict = {}
    # print(df_player1)
    # pdb.set_trace()
    for col in RELATIVE_COL + ABSOLUTE_COL:
        player1_col = df_player1[col]
        player2_col = df_player2[col]

        player1_col = float(player1_col.to_numpy().squeeze())
        player2_col = float(player2_col.to_numpy().squeeze())

        # print(player2_col)
        if col in RELATIVE_COL:
            stat_comparison = {col: relative_comparison(player1_col, player2_col)}
        else:
            stat_comparison = {col: absolute_comparison(player1_col, player2_col)}
        # print(stat_comparison)
        stats_comparison_dict.update(stat_comparison)

    return stats_comparison_dict

def collect_player_name():
    player1_name_for_function = ""
    player_name_checker = "Did you mean {}?"
    while player1_name_for_function not in df_player_database:
        player1_name = input("Enter the first player's name: ")
        player1_name_for_function = (
            player1_name.lower()[: player1_name.find(" ")]
            + "-"
            + player1_name.lower()[player1_name.find(" ") + 1 :]
        )
        print(player1_name)

        if player1_name_for_function in df_player_database:
            return player1_name
        
        print("Player name not found in database.")
        player1_closest_name = find_closest_string(player1_name_for_function)
        is_closest_name = input(player_name_checker.format(player1_closest_name)) #make it a boolean
        if is_closest_name == "Yes":
            return player1_closest_name
    
    
        
def find_closest_string(proposed_string):
    highest = 0
    for name in df_player_database.Name:
        current = SequenceMatcher(None, proposed_string, name).ratio()
        if current > highest:
            highest = current
            highest_name = name
    return highest_name

    

df_basic_stats = make_dataset(
    "C:/Users/klako/OneDrive/Documents/Polygence_Project/basic_stats"
)
df_advanced_stats = make_dataset(
    "C:/Users/klako/OneDrive/Documents/Polygence_Project/advanced_stats", offset=13
)
# df_basic_stats.join(df_advanced_stats,on=["Name","Season"],how="outer")
df_player_database = df_basic_stats.merge(
    df_advanced_stats, how="left", on=["Name", "Season", "Tm"], suffixes=(None, "_a")
)
df_player_database.drop(
    df_player_database.columns[[31, 32, 33, 34, 35]], axis=1, inplace=True
)
df_player_database.drop(
    df_player_database.columns[
        [
            43,
            48,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
        ]
    ],
    axis=1,
    inplace=True,
)

print(df_player_database.shape[0])
df_player_database = df_player_database[
    ~df_player_database.Tm.str.contains("Did Not Play", na=False)
]
print(df_player_database.shape[0])
column_str = ["Name", "Season", "Age", "Tm", "Lg", "Pos"]
column_int = ["G", "GS"]
type_dict = {}
type_dict.update({name: "string" for name in column_str})
type_dict.update({name: "int32" for name in column_int})
type_dict.update(
    {
        name: "float64"
        for name in df_player_database.columns
        if name not in (column_str + column_int)
    }
)

# Input section of code
player1_name = collect_player_name()
player1_season = input("Enter the player's season (YYYY-YY): ")
print(player1_season)
player2_name = collect_player_name()
player2_season = input("Enter the player's season (YYYY-YY): ")
print(player2_season)

test_run = stat_checker(
    df_player_database,
    player1_name,
    player1_season,
    player2_name,
    player2_season,
)
for key in GROUP_DICT:
    print(key + " statistics")
    count = 0
    for param in GROUP_DICT[key]:
        value = test_run[param]
        if param in RELATIVE_COL:
            rel_string = "%"
        else:
            rel_string = ""
        string1 = "{} has a {:.2f}{} increase in {} compared to {}"
        if value > 0:
            print(string1.format(player2_name, value, rel_string, param, player1_name))
            count += 1
        elif value == 0:
            print("Both players are equal in " + param)
        else:
            print(string1.format(player1_name, -value, rel_string, param, player2_name))
            count -= 1
    if count > 0:
        print(player2_name + " is better than " + player1_name + " at " + key)
    elif count == 0:
        print("Both players are equally matched at " + key)
    else:
        print(player1_name + " is better than " + player2_name + " at " + key)

# pdb.set_trace()
# https://stackoverflow.com/questions/28679930/how-to-drop-rows-from-pandas-data-frame-that-contains-a-particular-string-in-a-p


# User inputs "Player1_name" and "Player1_Season"
# User inputs "Player2_name" and "Player2_Season"
