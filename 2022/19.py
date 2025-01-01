from aocd.get import get_data
from aocd.post import submit
from typing import NamedTuple
import _utils as util
import timeit
import math
import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
example1 = "Blueprint 1:  Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
example2 = "Blueprint 2:  Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian."
# print(data)
clean_data = data.split("\n")

resource_types = ['ore', 'clay', 'obsidian', 'geode'] #in increasing order of "value"

# need these for an optimisation later
def triangular_root(Tn:int) -> float:
    if Tn <= 0: return 0
    else:
        return math.ceil((-1 + pow((1+8*Tn), 0.5)) * 0.5)

def triangular_number(n:int) -> int:
    return n * (n + 1) / 2


class Blueprint():
    def __init__(self, bp_data):
        self.id = int(bp_data[0])
        self.robot_costs = {
            'ore':{'ore':int(bp_data[1])},
            'clay':{'ore':int(bp_data[2])},
            'obsidian':{'ore':int(bp_data[3]), 'clay':int(bp_data[4])},
            'geode':{'ore':int(bp_data[5]), 'obsidian':int(bp_data[6])},
        }
        self.max_required_income = {
            'ore':max(int(bp_data[1]),int(bp_data[2]),int(bp_data[3]),int(bp_data[5])),
            'clay':int(bp_data[4]),
            'obsidian':int(bp_data[6]),
        }
        self.min_time_to_robot = {
            'obsidian': triangular_root(self.robot_costs['obsidian']['clay']),
            'geode': triangular_root(self.robot_costs['geode']['obsidian']),
        }
    
    def buildable_robots(self, income:dict[str:int]) -> list:
        buildable_robots = []
        if income['obsidian'] > 0: buildable_robots.append('geode')
        if income['clay'] > 0: buildable_robots.append('obsidian')
        buildable_robots.extend(['clay', 'ore'])
        return buildable_robots


blueprint_data = [Blueprint(re.findall(util.re_get_ints, bp)) for bp in clean_data]

class State(NamedTuple):
    prior_state_index:int
    prior_state_robot_built:str
    time_left:int
    stock:dict[str:int] 
    income:dict[str:int]

    def to_tuple(self) -> tuple:
        return (
            self.time_left,
            self.stock['ore'],
            self.stock['clay'],
            self.stock['obsidian'],
            self.stock['geode'],
            self.income['ore'],
            self.income['clay'],
            self.income['obsidian'],
            self.income['geode'],
        )


def time_required(cost:dict[str:int], stock:dict[str:int], income:dict[str:int]):
    time_required_to_build = 1
    time_required_to_save = 0
    for r in cost:
        shortfall = cost[r] - stock[r]
        time_required_to_save = max(time_required_to_save, math.ceil(shortfall/income[r]))
    return time_required_to_build + time_required_to_save



def using_bfs_with_optimisations(time_given:int, blueprint:Blueprint):

    # triangular number lookup table
    triangular_numbers = {n:triangular_number(n) for n in range(time_given+1)}

    # set up the initial state
    stock = {r:0 for r in resource_types}
    income = stock.copy()
    income.update({'ore':1})
    costs = blueprint.robot_costs
    first_state = State(None, 'ore', time_given, stock.copy(), income.copy())

    # set up the state queue
    state_queue:list[State] = [first_state]
    states_seen:set[tuple] = set()
    max_geodes = 0
    max_geode_states:list[State] = []
    index = 0

    while index < len(state_queue):

        current_state = state_queue[index]
        current_stock = current_state.stock
        current_income = current_state.income
        time_left = current_state.time_left
        index += 1


        # OPTIMISATION #2: check if we have seen the state already
        # minimal/no improvement for bfs
        current_state_tuple = current_state.to_tuple()
        if current_state_tuple in states_seen: continue
        states_seen.add(current_state_tuple)


        # check if we are out of time
        if time_left == 0:
            if current_stock['geode'] >= max_geodes:
                max_geodes = current_stock['geode']
                max_geode_states.append(current_state)
            continue


        # OPTIMISATION #3: calculate a conservative lowerbound for geode potential
        # ~4x improvement
        # can do time_left - 1 because making a geode in the last min doesnt do anything
        geode_potential = current_stock['geode'] + current_income['geode'] * time_left + triangular_numbers[time_left - 1]
        if geode_potential <= max_geodes: continue


        buildable_robots = blueprint.buildable_robots(current_income)
        build_times = {
            r:time_required(costs[r], current_stock, current_income) for r in buildable_robots
        }

        for next_robot in buildable_robots:
            robot_cost:int = costs[next_robot]
            build_time:int = build_times[next_robot]

            # OPTIMISATION #1: dont build more robots that you will possibly need.
            # i.e. no point building the 5th ore robot if the max ore cost is 4.
            # ~20x improvement
            if next_robot in blueprint.max_required_income:
                if current_income[next_robot] >= blueprint.max_required_income[next_robot]:
                    continue
            
            if build_time >= time_left:
                final_stock = current_stock.copy()
                for r in current_income.keys():
                    final_stock[r] += time_left * current_income[r]
                next_state = State(index-1, next_robot, 0, final_stock.copy(), current_income.copy())
            
            if build_time < time_left:
                next_state_stock = current_stock.copy()
                for r in current_income.keys():
                    if r in robot_cost: cost = robot_cost[r]
                    else: cost = 0
                    next_state_stock[r] += build_time * current_income[r] - cost
                next_state_income = current_income.copy()
                next_state_income[next_robot] += 1
                next_state = State(index-1, next_robot, time_left - build_time, next_state_stock.copy(), next_state_income.copy())
            
            state_queue.append(next_state)

    state_sequences:list[list[State]] = []
    for state in max_geode_states:
        if state.stock['geode'] < max_geodes:
            continue
        current_state = state
        sequence:list[State] = []
        while current_state.prior_state_index != None:
            sequence.append(current_state)
            current_state = state_queue[current_state.prior_state_index]
        sequence.reverse()
        state_sequences.append(sequence)
    print("Blueprint",blueprint.id,"mined",max_geodes,"geodes! The quailty of this blueprint is",blueprint.id*max_geodes)

    return max_geodes, state_sequences


def using_dfs_with_optimisations(time_given:int, blueprint:Blueprint):

    # triangular number lookup table
    triangular_numbers = {n:triangular_number(n) for n in range(time_given+1)}
    
    # set up the initial state
    stock = {r:0 for r in resource_types}
    income = stock.copy()
    income.update({'ore':1})
    costs = blueprint.robot_costs
    first_state = State(None, 'ore', time_given, stock.copy(), income.copy())
    
    # set up the state queue
    state_stack:list[State] = [first_state]
    states_seen:set[tuple] = set()
    state_sequences:list[list[State]] = []
    max_geodes = 0
    max_geode_states:list[State] = []

    while len(state_stack) > 0:
        index = len(state_stack) - 1
        current_state = state_stack[index]
        current_stock = current_state.stock
        current_income = current_state.income
        time_left = current_state.time_left


        # OPTIMISATION #2: check if we have seen the state already
        # this step is not really an optimisation here as it is required for dfs
        # otheriwse it will just re-expand the same node forever
        current_state_tuple = current_state.to_tuple()
        if current_state_tuple in states_seen:
            state_stack.pop()
            continue
        states_seen.add(current_state_tuple)


        # check if we are out of time
        if time_left == 0:
            if current_stock['geode'] >= max_geodes:
                max_geodes = current_stock['geode']
                max_geode_states.append(current_state)
            
            sequence:list[State] = []
            while current_state.prior_state_index != None:
                sequence.append(current_state)
                current_state = state_stack[current_state.prior_state_index]
            sequence.reverse()
            state_sequences.append(sequence)

            state_stack.pop()
            continue


        # OPTIMISATION #3: calculate a conservative lowerbound for geode potential
        # ~4x improvement
        # can do time_left - 1 because making a geode in the last min doesnt do anything
        geode_potential = current_stock['geode'] + current_income['geode'] * time_left + triangular_numbers[time_left - 1]
        if geode_potential <= max_geodes:
            state_stack.pop()
            continue


        buildable_robots = blueprint.buildable_robots(current_income)
        build_times = {
            r:time_required(costs[r], current_stock, current_income) for r in buildable_robots
        }

        
        for next_robot in buildable_robots:
            robot_cost:int = costs[next_robot]
            build_time:int = build_times[next_robot]

            # OPTIMISATION #1: dont build more robots that you will possibly need.
            # i.e. no point building the 5th ore robot if the max ore cost is 4.
            # ~20x improvement
            if next_robot in blueprint.max_required_income:
                if current_income[next_robot] >= blueprint.max_required_income[next_robot]:
                    continue
            
            if build_time >= time_left:
                final_stock = current_stock.copy()
                for r in current_income.keys():
                    final_stock[r] += time_left * current_income[r]
                next_state = State(index, next_robot, 0, final_stock.copy(), current_income.copy())
            
            if build_time < time_left:
                next_state_stock = current_stock.copy()
                for r in current_income.keys():
                    if r in robot_cost: cost = robot_cost[r]
                    else: cost = 0
                    next_state_stock[r] += build_time * current_income[r] - cost
                next_state_income = current_income.copy()
                next_state_income[next_robot] += 1
                next_state = State(index, next_robot, time_left - build_time, next_state_stock.copy(), next_state_income.copy())
            
            state_stack.append(next_state)

    state_sequences = [s for s in state_sequences if s[-1].stock['geode'] == max_geodes]
    
    print("Blueprint",blueprint.id,"mined",max_geodes,"geodes! The quailty of this blueprint is",blueprint.id*max_geodes)

    return max_geodes, state_sequences



#part 1:
# dfs vs bfs made minimal difference for part 1
print("Starting part 1...")
bp_example1 = Blueprint(re.findall(util.re_get_ints, example1))
bp_example2 = Blueprint(re.findall(util.re_get_ints, example2))

time_given1 = 24
simulations1 = []

total_duration1 = 0
for bp in blueprint_data:
    start = timeit.default_timer()
    g, seq = using_dfs_with_optimisations(time_given1, bp)
    duration = timeit.default_timer() - start
    total_duration1 += duration
    simulations1.append((duration, bp, g, seq))

ans1 = sum([n[2]*n[1].id for n in simulations1])
print("Part 1 took", total_duration1,"seconds")
# submit(ans1,1,day,year)


#part 2:
# as expected, using dfs was ~10x faster for part 2!
# this is because we prune branches based on the best result so far
# dfs reaches a "good" answer quicker and can prune more aggressively
print("Starting part 2...")
time_given2 = 32
simulations2 = []

total_duration2 = 0
for bp in blueprint_data[0:3]:
    start = timeit.default_timer()
    g, seq = using_dfs_with_optimisations(time_given2, bp)
    duration = timeit.default_timer() - start
    total_duration2 += duration
    simulations2.append((duration, bp, g, seq))

ans2 = 1
for s in simulations2:
    ans2 *= s[2]
print("Part 2 took", total_duration2, "seconds")
# submit(ans2,2,day,year)

pass