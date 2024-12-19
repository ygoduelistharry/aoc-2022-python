from aocd.get import get_data
from aocd.post import submit
# from ast import literal_eval as leval
# import numpy as np
# import polars as pl
import _utils as util
# import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

#part 1:

class Block():
    def __init__(self, type):
        self.type = type
        match type:
            case '_': #these are in ROW COL format (ie, y,x)
                self.relative_blocks = {(0,0),(0,1),(0,2),(0,3)}
            case '+':
                self.relative_blocks = {(0,1),(1,0),(1,1),(1,2),(2,1)}
            case 'J':
                self.relative_blocks = {(0,0),(0,1),(0,2),(1,2),(2,2)}
            case 'I':
                self.relative_blocks = {(0,0),(1,0),(2,0),(3,0)}
            case 'O':
                self.relative_blocks = {(0,0),(0,1),(1,0),(1,1)}
            case _:
                print("Shouldn't be able to get here..")
        self.height = max([coord[0] for coord in self.relative_blocks])

block_types = [Block(shape) for shape in ['_', '+','J', 'I', 'O']]
max_tower_height = -1
block_count = 0
move_count = 0
chamber_width = 7
drop_height = 4
drop_col = 2
empty_row = [0 for _ in range(chamber_width)]
tower = [empty_row.copy()]

need_new_block = True

#load of optimisations to do (might need them for part 2...), but it's already pretty fast:
# - first 3 falls of every piece are guaranteed to be fine
# - keep track of the left/rightmost positions to avoid checking EVERYTHING for walls
# - theres probably some bitwise and/or stuff you could do

while block_count <= 2022:

    if need_new_block:
        falling_block = block_types[block_count % len(block_types)]
        while len(tower) <= max_tower_height + falling_block.height + drop_height:
            tower.append(empty_row.copy())
        block_count += 1
        falling_block_position = {(y+max_tower_height+drop_height, x+drop_col) for (y,x) in falling_block.relative_blocks}
        need_new_block = False

    move = data[move_count % len(data)]
    move_count += 1
    can_move = True
    if move == '<':
        for (y,x) in falling_block_position:
            if x == 0 or tower[y][x-1] == 1:
                can_move = False
                break
        if can_move:
            falling_block_position = {(pos[0], pos[1] - 1) for pos in falling_block_position}
    
    if move == '>':
        for (y,x) in falling_block_position:
            if x == chamber_width - 1 or tower[y][x+1] == 1:
                can_move = False
                break
        if can_move:
            falling_block_position = {(pos[0], pos[1] + 1) for pos in falling_block_position}
    
    for (y,x) in falling_block_position:
        if y == 0 or tower[y-1][x] == 1:
            need_new_block = True
            break
    if need_new_block:
        for (y,x) in falling_block_position:
            tower[y][x] = 1
            max_tower_height = max(max_tower_height, y)
    else:
        falling_block_position = {(pos[0] - 1, pos[1]) for pos in falling_block_position}

ans1 = max_tower_height + 1

submit(ans1,1,day,year)

#part 2:
#submit(ans2,2,day,year)

pass