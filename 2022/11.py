from aocd.get import get_data
from aocd.post import submit
from math import lcm
import numpy as np
import re
from collections import deque
day = 11
year = 2022
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

# un-understandable python :)
monkey_items = [deque([int(item) for item in re.findall(r'\d+(?=,?)',clean_data[monkey*7+1])]) for monkey in range(8)]
monkey_items1 = [deque([int(item) for item in re.findall(r'\d+(?=,?)',clean_data[monkey*7+1])]) for monkey in range(8)]
monkey_items2 = [deque([int(item) for item in re.findall(r'\d+(?=,?)',clean_data[monkey*7+1])]) for monkey in range(8)]
monkey_operations = [
    lambda i:i*2,
    lambda i:i+3,
    lambda i:i+6,
    lambda i:i+5,
    lambda i:i+8,
    lambda i:i*5,
    lambda i:i*i,
    lambda i:i+4
]
monkey_tests = [
    lambda i:i%17 == 0,
    lambda i:i%13 == 0,
    lambda i:i%19 == 0,
    lambda i:i%7 == 0,
    lambda i:i%11 == 0,
    lambda i:i%3 == 0,
    lambda i:i%2 == 0,
    lambda i:i%5 == 0
]
test_lcm = lcm(17,13,19,7,11,3,2,5)

monkey_throw_to = [
    [2,5],
    [7,4],
    [6,5],
    [7,1],
    [0,2],
    [6,3],
    [3,1],
    [4,0]
]


def check_and_throw(monkey_items, monkey, relief = 3):
    item = monkey_items[monkey].popleft()
    item = monkey_operations[monkey](item)
    item = int(item)//int(relief)
    item = item%test_lcm
    if monkey_tests[monkey](item):
        monkey_items[monkey_throw_to[monkey][0]].append(item)
    else:
        monkey_items[monkey_throw_to[monkey][1]].append(item)
    return monkey_items

monkey_check_count1 = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]

monkey_check_count2 = monkey_check_count1.copy()

for turn in range(20):
    for monkey in range(8):
        while len(monkey_items1[monkey]) > 0:
            monkey_items1 = check_and_throw(monkey_items1, monkey)
            monkey_check_count1[monkey] += 1

monkey_check_count1.sort()
ans1 = monkey_check_count1[-1]*monkey_check_count1[-2]

#part 1:
#submit(ans1,1,day,year)


for turn in range(10000):
    for monkey in range(8):
        while len(monkey_items2[monkey]) > 0:
            monkey_items2 = check_and_throw(monkey_items2, monkey, relief=1)
            monkey_check_count2[monkey] += 1

monkey_check_count2.sort()
ans2 = monkey_check_count2[-1]*monkey_check_count2[-2]

#part 2:
submit(ans2,2,day,year)

pass