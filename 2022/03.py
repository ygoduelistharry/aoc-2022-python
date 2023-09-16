from aocd.get import get_data
from aocd.post import submit

data = get_data(day=3, year=2022)
print(data)

rucksack_list = data.split("\n")
    
for id, rucksack in enumerate(rucksack_list):
    mid = int(len(rucksack)/2)
    rucksack_list[id] = [rucksack[0:mid],rucksack[mid:len(rucksack)]]

def find_matching_element(a, b, c=None):
    
    set_a = set(a)
    set_b = set(b)
    if c is not None:
        set_c = set(c)
    
    if c is None:
        for char in set_a:
            if char in set_b:
                return char

    for char in set_a:
        if char in set_b and char in set_c:
            return char
    
    return

def priority(char):
    if ord(char)>=97:
        return ord(char) - 96
    if ord(char)>=65:
        return ord(char) - 38

priority_sum = 0

for rucksack in rucksack_list:
    c1 = rucksack[0]
    c2 = rucksack[1]
    priority_sum += priority(find_matching_element(c1,c2))

#part 1
submit(priority_sum,1,3,2022)


rucksack_list_2 = data.split("\n")

for id, rucksack in enumerate(rucksack_list_2):
    rucksack_list_2[id] = set(rucksack)

n = 3
elf_groups = [rucksack_list_2[i:i+n] for i in range(0, len(rucksack_list_2), n)]

priority_sum_2 = 0
for group in elf_groups:
    c1 = group[0]
    c2 = group[1]
    c3 = group[2]
    priority_sum_2 += priority(find_matching_element(c1,c2,c3))

#part 2
submit(priority_sum_2,2,3,2022)

pass