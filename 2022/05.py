from aocd.get import get_data
from aocd.post import submit
from copy import deepcopy
day = 5
year = 2022
data = get_data(day=day, year=year)
print(data)

stack_data = data.split("\n")[0:8]

def parse_stack(stack_list, n):
    stack = []
    pos = 1+4*n
    for row in stack_list:
        if row[pos] != " ":
            stack.append(row[pos])
    
    stack.reverse()
    return stack

stacks = []
for n in range(9):
    stacks.append(parse_stack(stack_data,n))
stacks2 = deepcopy(stacks)

move_data = data.split("\n")[10:]

def make_moves(stacks, move, sep=True):
    tokens = move.split(" ")
    qty = int(tokens[1])
    src = int(tokens[3])-1
    des = int(tokens[5])-1

    if sep:
        for m in range(qty):
            stacks[des].append(stacks[src].pop())
    else:
        stacks[des] += stacks[src][-qty:]
        stacks[src] = stacks[src][:-qty]

for move in move_data:
    make_moves(stacks, move)

ans1 = ''
for stack in stacks:
    ans1 += stack[-1]

#part 1:
submit(ans1,1,day,year)

for move in move_data:
    make_moves(stacks2, move, sep=False)

ans2 = ''
for stack in stacks2:
    ans2 += stack[-1]

#part 2:
submit(ans2,2,day,year)

pass