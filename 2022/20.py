from aocd.get import get_data
from aocd.post import submit
from ast import literal_eval as leval
from collections import deque
import numpy as np
import polars as pl
import _utils as util
import timeit
import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")
example_data = [1,2,-3,3,-2,0,4]

# probably need a linked list
# in python, deque from collections is implemented as a linked list

# since there are duplicate values in the data we need to also track their original index
# this ensures uniqueness when searching the linked list
initial_arrangement = [(i,int(n)) for i, n in enumerate(clean_data)]
example_arrangement = [(i,example_data[i]) for i in range(len(example_data))]


def mix_it_up(initial_arrangement:list[tuple[int,int]], mix_times:int = 1) -> deque[tuple[int,int]]:
    mixed_arrangement = deque(initial_arrangement)
    for _ in range(mix_times):
        for n in initial_arrangement:
            i = mixed_arrangement.index(n)
            if n[1] == 0: continue
            mixed_arrangement.remove(n)
            mixed_arrangement.insert((i+n[1])%len(mixed_arrangement), n)
    return mixed_arrangement

def sum_the_coordinates(mixed_arrangement:deque[int]) -> int:
    for i, n in enumerate(mixed_arrangement):
        if n[1] == 0:
            break
    coords = []
    for j in [1000,2000,3000]:
        coords.append(mixed_arrangement[(i+j)%len(mixed_arrangement)][1])
    print(coords)
    return sum(coords)


#part 1:
arrangement1 = initial_arrangement.copy()
mixed1 = mix_it_up(arrangement1)
ans1 = sum_the_coordinates(mixed1)
# submit(ans1,1,day,year)

#part 2:
key = 811589153
arrangement2 = [(n[0],n[1]*key) for n in initial_arrangement]
mixed2 = mix_it_up(arrangement2, 10)
ans2 = sum_the_coordinates(mixed2)
# submit(ans2,2,day,year)

pass