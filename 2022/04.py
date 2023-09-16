from aocd.get import get_data
from aocd.post import submit

data = get_data(day=4, year=2022)

clean_data = data.split("\n")
for i, elf_pair in enumerate(clean_data):
    clean_data[i] = elf_pair.split(",")
    clean_data[i][0] = clean_data[i][0].split("-")
    clean_data[i][1] = clean_data[i][1].split("-")

def range_overlap(l1,u1,l2,u2,incl=True,full=True):
    l1 = int(l1)
    u1 = int(u1)
    l2 = int(l2)
    u2 = int(u2)

    r1 = set(range(l1,u1+incl))
    r2 = set(range(l2,u2+incl))
    u = r1.union(r2)

    if full:
        if len(u) == max(len(r1),len(r2)):
            return True
    
    if len(u) == len(r1)+len(r2):
        return False
    
    return True

ans1 = 0
for i in clean_data:
    if range_overlap(i[0][0],i[0][1],i[1][0],i[1][1]):
        ans1+=1

#part 1:
submit(ans1,1,4,2022)

ans2 = 0
for i in clean_data:
    if range_overlap(i[0][0],i[0][1],i[1][0],i[1][1],full=False):
        ans2+=1

#part 2:
submit(ans2,2,4,2022)

pass