from aocd.get import get_data
from aocd.post import submit

data = get_data(day=1, year=2022)

items = data.split("\n")
total_calories = [0]

for item in items:
    if item == "":
        total_calories.append(0)
    else:
        total_calories[-1] = total_calories[-1] + int(item)

max_cals = max(total_calories)
elf_with_most_calories = total_calories.index(max_cals)+1

#part 1:
submit(max_cals,1,1,2022)

total_calories.sort(reverse=True)
top_3_elves = total_calories[0:3]

#part 2:
submit(sum(top_3_elves),2,1,2022)

pass