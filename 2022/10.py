from aocd.get import get_data
from aocd.post import submit
import numpy as np
day = 10
year = 2022
data = get_data(day=day, year=year)
#print(data)
clean_data = data.split("\n")

reg_start = 1
cycle = 0
cache = [0]

def append_cycle(instruction:str, cache:list):
    new_cache = cache.copy()
    if instruction == 'noop':
        new_cache.append(0)
    if instruction[:4] == 'addx':
        i = instruction.split(" ")
        new_cache.append(0)
        new_cache.append(int(i[1]))
    return new_cache

def signal_at_cycle(start:int, cycle:int, cache:list):
    return (sum(cache[:cycle]) + start)*cycle

cache1 = cache.copy()
for i in clean_data:
    cache1 = append_cycle(i, cache1)

ans1 = 0
for c in [20, 60, 100, 140, 180, 220]:
    ans1 += signal_at_cycle(reg_start, c, cache1)

#part 1:
submit(ans1,1,day,year)

#part 2:
crt = ['#']
running_regx = [reg_start]
for k, v in enumerate(cache1):
    if k != 0:
        r = v+running_regx[k-1]
        running_regx.append(r)
        if abs(k%40-r) <= 1:
            crt.append("#")
        else:
            crt.append('.')

for row in range(6):
    print(crt[row*40:(row+1)*40])

ans2 = "PZGPKPEB"

submit(ans2,2,day,year)
pass