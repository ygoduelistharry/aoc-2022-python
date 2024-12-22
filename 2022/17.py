from aocd.get import get_data
from aocd.post import submit
import _utils as util
import itertools
from collections import namedtuple
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

# part 1/2:
# bitwise solution for checking collision
# each row can be represented as a single integer and be operated on with bitwise op
# the tower likely just repeats itself at some point, so uses a cache of states to detect a repeat

# eg if the tower row looks like [..#.##.], then the integer representing it will be c[2] + c[4] + c[5] = 20
c = [64,32,16,8,4,2,1]
full_row = sum(c)
empty_row = 0
# a tower is just a list of ints
# the height of the tower will correspond to the largest list index with a value > 0
empty_tower = [full_row, empty_row, empty_row, empty_row, empty_row, empty_row, empty_row, empty_row]
# parameters from the question
drop_col = 2
drop_height = 4 # 3 empty spaces plus the bottom of the new block itself
chamber_width = len(c)
# there's not enough moves to last 1mil blocks so we loop around to the start when we run out
# this is no problem, except we process 4 moves at a time when a new block appears for efficiency
# when we are within 4 blocks of the end of a list, taking a slice 4 long will try to access the list out of bounds
# to solve this, we just add the first 4 moves to the end
long_data = data + data[0:4]
block_types = ['_', '+','j', 'i', 'o']
# the default block shape data assumes they are as far left as possible in the row
# the 'origin' of a piece is the bottom left corner (for a +, this square is empty, but is still the origin)
# we will bit shift them right or left after horizontal moves
blocks = {
    '_':[sum(c[0:4])],
    '+':[c[1], sum(c[0:3]), c[1]],
    'j':[sum(c[0:3]), c[2], c[2]],
    'i':[c[0], c[0], c[0], c[0]],
    'o':[sum(c[0:2]), sum(c[0:2])],
}
# useful stuff
block_widths = {
    '_':4,
    '+':3,
    'j':3,
    'i':1,
    'o':2,
}
block_heights = {block:len(rows) for block, rows in blocks.items()}

# function is written to handle a sequence of horizontal shifts (but NO falling)
# we can safely process the first 4 moves after a block appears
# all further moves must be done one at a time with a fall check in between
# when processing multiple moves at once, it returns and integer representing the column the piece ends up in
def process_horizontal_shift(tower:list[int], block:str, curr_origin_row:int, curr_origin_col:int, moves:list[str]):
    for move in moves:
        can_move = True
        if move == '<' and curr_origin_col > 0:
            for i, block_row in enumerate(blocks[block]):
                # remember blocks start on the far left
                # so they must be shifted to where they actually are, then one to the left (or right)
                block_row_shifted = block_row >> curr_origin_col - 1
                tower_row = tower[curr_origin_row + i]
                # the magic: python treats positive integers as True and 0 as False
                # if there is a collision, this will be > 0 and 0 if there is not
                if block_row_shifted & tower_row:
                    can_move = False
                    break
            if can_move:
                curr_origin_col -= 1

        if move == '>' and curr_origin_col + block_widths[block] < chamber_width:
            for i, block_row in enumerate(blocks[block]):
                block_row_shifted = block_row >> curr_origin_col + 1
                tower_row = tower[curr_origin_row + i]
                if block_row_shifted & tower_row:
                    can_move = False
                    break
            if can_move:
                curr_origin_col += 1
    
    return curr_origin_col

# same as horizontal but checks the relevant rows below the blocks position
# only processes 1 fall at a time
def process_fall(tower:list[int], block:str, curr_origin_row:int, curr_origin_col:int):
    if block == '+': bottom_rows = 2
    else: bottom_rows = 1
    for i, block_row in enumerate(blocks[block][0:bottom_rows]):
        tower_row_below = tower[curr_origin_row + i - 1]
        if block_row >> curr_origin_col & tower_row_below:
            return curr_origin_row, False
    return curr_origin_row - 1, True

# we pre-calculate the final column position of every new block after every possible 4 move sequence (there are 16).
# saves a lot of time (75%?) as every block can do 4 moves risk free at the start
four_move_horizontal_shifts = {}
for block in block_types:
    four_move_horizontal_shifts.update({
        block:{''.join(seq):process_horizontal_shift(empty_tower, block, drop_height, drop_col, seq)
        for seq in map(list, itertools.product(['>','<'], repeat=4))}
    })

# processing 1 trillion block via simulation is very time prohibitive
# since we know the moves and blocks follow a set, repeating pattern, there is likely going to be a repeating tower pattern too
# pieces can fall down gaps and do all sorts of things that dont impact tower height
# however, we can check for repeats when a tower row becomes full
# if this happens and we are at the same position in the move sequence, and at the same block in the block squence..
# the tower will repeat itself from now on!!

# necessary data to store after every block fall until we find a repeating pattern
State = namedtuple('State', ['tower_height', 'block_count', 'move_pointer', 'current_block'])

def process_blocks(total_blocks, starting_tower:list[int] = empty_tower, with_memo_check = True):
    tower = starting_tower.copy()
    max_tower_height = 0
    block_count = 0
    move_count = 0
    need_new_block = True
    state_cache:list[State[int,int,int,str]] = []
    while block_count < total_blocks:
        memo_check = False
        move_pointer = move_count % len(data) # moves repeat after a while, so take the mod
        if need_new_block:
            current_block = block_types[block_count % len(block_types)]
            move = None
            while len(tower) < max_tower_height + block_heights[current_block] + 1:
                tower.append(empty_row) # make enough empty space to accomodate worst case
            block_count += 1
            next_4_moves = long_data[move_pointer:move_pointer+4] #avoid access out of list bounds
            y0 = max_tower_height + 1
            x0 = four_move_horizontal_shifts[current_block][next_4_moves] #pre-processed first 4 moves
            move_count += 4
            need_new_block = False
        else:
            move = data[move_pointer]
            move_count += 1
            x0 = process_horizontal_shift(tower, current_block, y0, x0, [move])
        y0, did_fall = process_fall(tower, current_block, y0, x0)
        if not did_fall:
            for i, block_row in enumerate(blocks[current_block]):
                tower[y0 + i] += block_row >> x0
                if tower[y0 + i] == full_row and with_memo_check:
                    memo_check = True #check the cache if we make a full row
            max_tower_height = max(max_tower_height, y0 + block_heights[current_block] - 1)
            state_cache.append(State(max_tower_height, block_count, move_pointer, current_block))
            need_new_block = True
        
        #compare pointer and current block to all states. if they match, we have a repeating pattern since then
        if memo_check:
            current_state = state_cache[-1]
            for s in range(len(state_cache) - 1):
                if (state_cache[s].move_pointer, state_cache[s].current_block) == (current_state.move_pointer, current_state.current_block):
                # each repeating sequence will add some amount of height
                    height_change_since_last_same_state = current_state.tower_height - state_cache[s].tower_height
                # and will repeat after a certain amount of blocks
                    blocks_since_last_same_state = current_state.block_count - state_cache[s].block_count
                # so figure out how many blocks there are to go
                    blocks_until_target = total_blocks - current_state.block_count
                # find out how many times you need to repeat the sequence
                # and how many further blocks there are to process (the sequence is unlikely to divide evenly into what's left)
                    (iterations, remaining_blocks) = divmod(blocks_until_target, blocks_since_last_same_state)
                    max_tower_height += (
                # add the sequence height a bunch of times
                        iterations * height_change_since_last_same_state
                # use the state cache to find the tower height after a remainder more blocks and add that difference
                        + state_cache[s+int(remaining_blocks)].tower_height - state_cache[s].tower_height
                    )
                    return max_tower_height

    return max_tower_height

block_count_1 = 2_022
block_count_2 = 1_000_000_000_000
ans1 = process_blocks(block_count_1)
ans2 = process_blocks(block_count_2)


# submit(ans1,1,day,year)
# submit(ans2,2,day,year)

pass