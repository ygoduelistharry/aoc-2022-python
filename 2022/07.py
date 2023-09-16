from aocd.get import get_data
from aocd.post import submit
day = 7
year = 2022
data = get_data(day=day, year=year)
print(data)

clean_data = data.split("\n")

cd_cache = []
dir_sizes = {"/":0}

for i, inst in enumerate(clean_data):
    if inst.count("$ cd"):
        if inst.count(".."):
            cd_cache.pop()
            print(cd_cache)
        elif inst.count("/"):
            cd_cache = ["/"]
        else:
            cd_cache.append(cd_cache[-1]+inst[5:])
            dir_sizes[cd_cache[-1]] = 0
            print(cd_cache)
    
    if inst[0].isdigit():
        size = int(inst.split(" ")[0])
        for d in cd_cache:
            dir_sizes[d] += size

ans1 = sum(filter(lambda x: (x<=100000), dir_sizes.values()))

#part 1:
submit(ans1,1,day,year)

s = dir_sizes['/'] - 40000000
ans2 = min(filter(lambda x: (x>=s), dir_sizes.values()))

#part 2:
submit(ans2,2,day,year)
pass