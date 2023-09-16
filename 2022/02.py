from aocd.get import get_data
from aocd.post import submit

data = get_data(day=2, year=2022)
print(data)

rps_keys = {
    "A": "r",
    "B": "p",
    "C": "s",
    "X": "r",
    "Y": "p",
    "Z": "s"
}

scores_throw = {
    "r":1,
    "p":2,
    "s":3
}

scores_result = {
    "w":6,
    "d":3,
    "l":0
}

rps_game_data = data

for key in rps_keys:
    rps_game_data = rps_game_data.replace(key, rps_keys[key])

def game_result(you, opp):
    if you == opp:
        return scores_result["d"]
    
    if you == "r":
        if opp == "s":
            return scores_result["w"]
        else:
            return scores_result["l"]
    if you == "p":
        if opp == "r":
            return scores_result["w"]
        else:
            return scores_result["l"]
    if you == "s":
        if opp == "p":
            return scores_result["w"]
        else:
            return scores_result["l"]
    
    
    
rps_game_list = rps_game_data.split("\n")

for index, game in enumerate(rps_game_list):
    rps_game_list[index] = game.split(" ")

def total_score(game_list):
    score = 0
    for game in game_list:
        score += scores_throw[game[1]]
        score += game_result(game[1], game[0])
    
    return score

#part 1
submit(total_score(rps_game_list),1,2,2022)


rps_keys_2 = {
    "A": "r",
    "B": "p",
    "C": "s"
}

win_key = {
    "r":"s",
    "p":"r",
    "s":"p"
}

lose_key = {
    "r":"p",
    "p":"s",
    "s":"r"
}

rps_game_data_2 = data

for key in rps_keys_2:
    rps_game_data_2 = rps_game_data_2.replace(key, rps_keys_2[key])

rps_game_list_2 = rps_game_data_2.split("\n")

for index, game in enumerate(rps_game_list_2):
    rps_game_list_2[index] = game.split(" ")

    match rps_game_list_2[index][1]:
        case "X":
            rps_game_list_2[index][1] = win_key[rps_game_list_2[index][0]]
        case "Y":
            rps_game_list_2[index][1] = rps_game_list_2[index][0]
        case "Z":
            rps_game_list_2[index][1] = lose_key[rps_game_list_2[index][0]]
        
#part 2
submit(total_score(rps_game_list_2),2,2,2022)


pass