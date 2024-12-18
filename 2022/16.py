from aocd.get import get_data
from aocd.post import submit
from ast import literal_eval as leval
import numpy as np
import polars as pl
import _utils as util
import copy
import re
import os
import itertools
import timeit

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
example_data = (
'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB \nValve BB has flow rate=13; tunnels lead to valves CC, AA \nValve CC has flow rate=2; tunnels lead to valves DD, BB \nValve DD has flow rate=20; tunnels lead to valves CC, AA, EE \nValve EE has flow rate=3; tunnels lead to valves FF, DD \nValve FF has flow rate=0; tunnels lead to valves EE, GG \nValve GG has flow rate=0; tunnels lead to valves FF, HH \nValve HH has flow rate=22; tunnel leads to valve GG \nValve II has flow rate=0; tunnels lead to valves AA, JJ \nValve JJ has flow rate=21; tunnel leads to valve II'
)
use_example_data = False
if use_example_data: data = example_data
clean_data = data.split("\n")
for data in sorted(clean_data):
    print(data)

#part 1:

class Node():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.paths:dict[str,int] = {}

#populate a dict of valves
valve_dict:dict[str,Node] = {}
for valve in clean_data:
    valve_names = re.findall(r'[A-Z]{2}', valve)
    flow_rate = int(re.findall(util.re_get_ints, valve)[0])
    name = valve_names[0]
    to_valves = valve_names[1:]

    valve_dict.update({name:Node(name, flow_rate)})
    valve_dict[name].paths.update({n:1 for n in to_valves})


# remove irrelevant valves (0 flow and only 2 tunnels)
for from_valve, _ in valve_dict.copy().items():
    to_valves = [v for v in valve_dict[from_valve].paths.keys()]
    flow_rate = valve_dict[from_valve].value
    if len(to_valves) == 2 and flow_rate == 0:
        v1 = to_valves[0]
        v2 = to_valves[1]
        valve_dict[v1].paths[v2] = valve_dict[v1].paths.pop(from_valve) + valve_dict[from_valve].paths[v2]
        valve_dict[v2].paths[v1] = valve_dict[v2].paths.pop(from_valve) + valve_dict[from_valve].paths[v1]
        valve_dict.pop(from_valve)


# find distance between all valve pairs
def shortest_dists(source:str, nodes:dict[str,Node]):
    # use djikstra n times
    unvisited_nodes = {node for node in nodes}
    current_min_dists = {node:None for node in nodes}
    current_min_dists[source] = 0

    while unvisited_nodes:
        unvisited_node_min_dists = {node:dist for node, dist in current_min_dists.items() if node in unvisited_nodes and dist is not None}
        this = min(unvisited_node_min_dists, key=unvisited_node_min_dists.get)
        for next, this_to_next in nodes[this].paths.items():
            source_to_this = current_min_dists[this]
            source_to_next = current_min_dists[next]
            if source_to_next is None:
                current_min_dists[next] = source_to_this + this_to_next
            else:
                current_min_dists[next] = min(source_to_this + this_to_next, source_to_next)
        unvisited_nodes.remove(this)
    
    return current_min_dists



# value functions:
def move_time_required(dist, move_speed, act_speed):
    return dist * move_speed + act_speed

def move_value(time_required, value_per_time, time_left, activated_valves, to_valve):
    if time_required > time_left or to_valve in activated_valves: return 0
    else: return (time_left - time_required) * value_per_time

def valid_moves(curr_valve, dist_mat, move_speed, act_speed, time_left, valve_on_status):
    moves = {}
    for to_valve in valve_dict:
        dist = dist_mat[curr_valve][to_valve]
        value_per_time = valve_dict[to_valve].value
        time_required = move_time_required(dist, move_speed, act_speed)
        value = move_value(time_required, value_per_time, time_left, valve_on_status, to_valve)
        if value <= 0:
            continue
        moves.update({to_valve:{'value':value, 'time_required':time_required}})
    return moves

#do simulations!
#start state:
start_score = 0
time_given = 30
start_valve = "AA"
start_active_valves = set()

start_state = (start_score, time_given, start_valve, start_active_valves.copy())

#global vars:
move_speed = 1
act_speed = 1
distance_matrix = {v:shortest_dists(v, valve_dict) for v in valve_dict}

#depth first search!
def depth_first_search(start_state:tuple[int,int,str,set] = start_state) -> dict[frozenset, int]:
    search_stack:list[tuple[int,int,str,set]] = []
    search_stack.append(start_state)
    results:dict[frozenset,int] = {}

    while search_stack:
        current_state = search_stack.pop()
        current_score = current_state[0]
        current_time_left = current_state[1]
        current_valve = current_state[2]
        current_active_valves = current_state[3]

        moves = valid_moves(current_valve, distance_matrix, move_speed, act_speed, current_time_left, current_active_valves)
        for to_valve, move_info in moves.items():
            new_score = current_score + move_info['value']
            new_time_left = current_time_left - move_info['time_required']
            new_active_valves = current_active_valves.copy()
            new_active_valves.add(to_valve)
            search_stack.append((new_score, new_time_left, to_valve, new_active_valves))

            fs_new_active_valves = frozenset(new_active_valves)
            if fs_new_active_valves in results:
                results[fs_new_active_valves] = max(new_score, results[fs_new_active_valves])
            else:
                results[fs_new_active_valves] = new_score
        
    return results


max_scores = depth_first_search()
ans1 = max(max_scores.values())

submit(ans1,1,day,year)      



#part 2:
start = timeit.default_timer()

start_state2 = (start_score, 26, start_valve, start_active_valves.copy())
max_scores2:dict[frozenset,int] = depth_first_search(start_state2)

#just check the sum of all pairs of max valve visit scores that don't share any valves in common.
#does a few optimisations to avoid having to check the disjoint, but it's pretty close to brute force
#this takes 20 seconds but there is definitely a better way
max_single_score = max(max_scores2.values())
max_double_score_so_far = max_single_score
for set1, score1 in max_scores2.items():
    #if you cant even beat the max so far by adding the best single score, then dont even worry.
    if score1 + max_single_score < max_double_score_so_far:
        continue
    for set2, score2 in max_scores2.items():
        if score1 + score2 < max_double_score_so_far:
            continue
        if set1.isdisjoint(set2):
            max_double_score_so_far = score1 + score2

end = timeit.default_timer()
duration = end - start

ans2 = max_double_score_so_far

submit(ans2,2,day,year)
pass