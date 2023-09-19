from aocd.get import get_data
from aocd.post import submit
import numpy as np

day = 9
year = 2022
data = get_data(day=day, year=year)
print(data)

instructions = data.split("\n")

for n, i in enumerate(instructions):
    instructions[n] = i.split(" ")

def chase_position(lead, tail):
    rel_pos = np.array(lead) - np.array(tail)
    rel_x = rel_pos[0]
    rel_y = rel_pos[1]
    t_new = tail
    if rel_x == 0:
        if rel_y > 0:
            t_new += [0,1]
        if rel_y < 0:
            t_new += [0,-1]
    if rel_y == 0:
        if rel_x > 0:
            t_new += [1,0]
        if rel_x < 0:
            t_new += [-1,0]
    if rel_x > 0:
        if rel_y > 0:
            t_new += [1,1]
        if rel_y < 0:
            t_new += [1,-1]
    if rel_x < 0:
        if rel_y > 0:
            t_new += [-1,1]
        if rel_y < 0:
            t_new += [-1,-1]

    return t_new

def travel(dir:str, length:int=2, current_positions:list[int]=None):
    match dir:
        case "U":
            d = np.array([0,1])
        case "D":
            d = np.array([0,-1])
        case "L":
            d = np.array([-1,0])
        case "R":
            d = np.array([1,0])

    #k_pos[0] = head, k_pos[-1] = tail
    if current_positions is None:
        new_pos = [np.array([0,0]) for k in range(length)]
    else:
        new_pos = current_positions

    new_pos[0] += d
    for k in range(1,length):
        if max(abs(new_pos[k] - new_pos[k-1])) < 2:
            break
        new_pos[k] = chase_position(new_pos[k-1],new_pos[k])

    return new_pos

visited_by_h = np.array([0,0])
visited_by_t = np.array([0,0])

knot_positions = [np.array([0,0]), np.array([0,0])]

for i in instructions:
    for steps in range(int(i[1])):
        knot_positions = travel(i[0], 2, knot_positions)
        visited_by_h = np.append(visited_by_h, knot_positions[0])
        visited_by_t = np.append(visited_by_t, knot_positions[-1])

ans1 = len(np.unique(visited_by_t.reshape(-1,2),axis=0))

#part 1:
submit(ans1,1,day,year)

visited_by_h2 = np.array([0,0])
visited_by_t2 = np.array([0,0])

knot_positions2 = [np.array([0,0]) for k in range(10)]

for i in instructions:
    for steps in range(int(i[1])):
        knot_positions2 = travel(i[0], 10, knot_positions2)
        visited_by_h2 = np.append(visited_by_h2, knot_positions2[0])
        visited_by_t2 = np.append(visited_by_t2, knot_positions2[-1])

ans2 = len(np.unique(visited_by_t2.reshape(-1,2),axis=0))

#part 2:
submit(ans2,2,day,year)

pass