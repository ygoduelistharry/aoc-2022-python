from aocd.get import get_data
from aocd.post import submit
from ast import literal_eval as leval
from collections import namedtuple
import numpy as np
from copy import deepcopy
import polars as pl
import _utils as util
import math
import timeit
import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")
example_data = [
'#.######',
'#>>.<^<#',
'#.<..<<#',
'#>v.><>#',
'#<^v^^>#',
'######.#',
]

# we are going to represent the map as a bit mask/board
# since the blizzards wrap around to the other side, we need a function to do bitshifts with wrapping
# there is probably a nicer way to do this but idk, this made sense to me
def wrapped_bitshift(n:int, n_size:int, shift_count:int, shift_right:bool = False) -> int:
    shift = shift_count % n_size
    if shift_right: m = (n >> shift) + (n << (n_size - shift))
    else: m = (n << shift) + (n >> (n_size - shift))
    return m & (2 ** n_size - 1)



class BitBoard():
    def __init__(self, input):
        self.board = self.create_bit_board(input)
        # the blizzards will be in the exact same state after a set period of time
        self.repeat_rate = math.lcm(self.row_count - 2, self.col_count - 2)
    
    def create_bit_board(self, input) -> dict[str,dict[str,list]]:
        self.row_count = len(input)
        self.col_count = len(input[0])     
        
        # every row and column will have 2 bitmasks, one for each blizzard direcation
        # one for left/up (bit shift left) and right/down (bit shift right)
        bit_board = {
            'row':{
                'left':[0 for _ in range(self.row_count)],
                'right':[0 for _ in range(self.row_count)],
            },
            'col':{
                'up':[0 for _ in range(self.col_count)],
                'down':[0 for _ in range(self.col_count)],
            },
        }
        
        # iterate over the symbols and add the postion as a mask to the appropriate mask 
        # we iterate left to right, i.e. starting at index 0
        # but the leftmost bit is the biggest, so we need to subtract the index from the row/col count before it becomes the exponent
        # could solve this more elegantly by iterating in reverse but whatever
        for r, row in enumerate(input):
            r_exp = self.row_count - r - 1
            for c, symbol in enumerate(row):
                c_exp = self.col_count - c - 1
                match symbol:
                    # wall positions get added to every mask
                    case '#':
                        bit_board['row']['left'][r] += 2**(c_exp)
                        bit_board['row']['right'][r] += 2**(c_exp)
                        bit_board['col']['up'][c] += 2**(r_exp)
                        bit_board['col']['down'][c] += 2**(r_exp)
                    case '<':
                        bit_board['row']['left'][r] += 2**(c_exp)
                    case '>':
                        bit_board['row']['right'][r] += 2**(c_exp)
                    case '^':
                        bit_board['col']['up'][c] += 2**(r_exp)
                    case 'v':
                        bit_board['col']['down'][c] += 2**(r_exp)
                    case _:
                        continue
        
        return bit_board


    def locate_blizzards(self, index:int, turn:int, axis='row', just_l=False, just_r=False) -> int:
        if axis == 'row': l, r, length, count = 'left', 'right', self.col_count, self.row_count
        if axis == 'col': l, r, length, count = 'up', 'down', self.row_count, self.col_count

        # make a mask of just wall positions
        wall_mask = 2**(length-1) + 1
        # we need to know how many tiles to bit shift (i.e. all except the walls)
        no_wall_len = length - 2

        # we cant go out of bounds so return a mask of all 1s if this is the case
        if index < 0 or index >= count:
            return 2**length - 1

        mask_l:int = self.board[axis][l][index]
        mask_r:int = self.board[axis][r][index]
        
        # nothing moves on the edges (they are walls) so dont shift the mask
        if index == 0 or index == count - 1:
            return mask_l
        
        # the rest of the function bashes the left/right or up/down blizzards into a single row/col mask
        # this is great if we just want to know where we cant go
        # however for part 2 we need to know where each of the 4 specific blizzard types end up
        # we can do this by setting the mask for the type we dont care about to 0
        if just_r: mask_l = 0
        if just_l: mask_r = 0
        
        # assume the lane in completely free except the fixed walls
        occupied_mask = wall_mask
        for dir, mask in enumerate([mask_l, mask_r]):
            if mask == 0: continue
            # remove the walls
            mask = (mask >> 1) & (2**no_wall_len - 1)
            # shift the bits with wrapping
            mask = wrapped_bitshift(mask, no_wall_len, turn, dir)
            # add the walls back
            # for some reason we get an overflow error when bit shifting left by 1, but not when multiplying by 2 ?????
            mask = mask * 2 + wall_mask
            # update the occupied mask with the new blizzard locations
            occupied_mask = occupied_mask | mask
        
        return occupied_mask

    def pprint(self):
        # makes the current state of the board somewhat readable
        print('left')
        for n in self.board['row']['left']:
            print(bin(n))
        print('right')
        for n in self.board['row']['right']:
            print(bin(n))
        print('up')
        for n in self.board['col']['up']:
            print(bin(n))
        print('down')
        for n in self.board['col']['down']:
            print(bin(n))

    
def get_new_bit_board_after_waiting(bit_board:BitBoard, n:int) -> BitBoard:
    # returns a new bit board after n minutes have passed
    # needed for part 2
    new_bit_board = deepcopy(bit_board)
    for axis, dir in bit_board.board.items():
        for d, masks in dir.items():
            if d == 'left' or d == 'up': just_l = True
            else: just_l = False
            if d == 'right' or d == 'down': just_r = True
            else: just_r = False
            for i in range(len(masks)):
                new_bit_board.board[axis][d][i] = bit_board.locate_blizzards(i, n, axis, just_l, just_r)

    return new_bit_board


def get_valid_moves(pos:tuple[int,int], bit_board:BitBoard, turn:int, start_pos:tuple[int,int], log = False) -> list[tuple[int,int]]:
    
    # we need to know where the blizzards will be after n turns for adjacent squares
    # we only need to know the current row/col and the adjacent 2 rows and cols

    this_row = bit_board.locate_blizzards(pos[0], turn, 'row')
    upper_row = bit_board.locate_blizzards(pos[0]-1, turn, 'row')
    lower_row = bit_board.locate_blizzards(pos[0]+1, turn, 'row')
    
    this_col = bit_board.locate_blizzards(pos[1], turn, 'col')
    left_col = bit_board.locate_blizzards(pos[1]-1, turn, 'col')
    right_col = bit_board.locate_blizzards(pos[1]+1, turn, 'col')

    pos_mask_row = 2 ** (bit_board.col_count - 1 - pos[1])
    pos_mask_col = 2 ** (bit_board.row_count - 1 - pos[0])

    valid_moves = set()
    # can always wait at the start
    if pos == start_pos: valid_moves.add(pos)

    # check the 5 potential move locations:
    # wait:
    if (this_row & pos_mask_row) | (this_col & pos_mask_col) == 0:
        valid_moves.add((pos[0], pos[1]))
    # right:
    if (this_row & pos_mask_row >> 1) | (right_col & pos_mask_col) == 0:
        valid_moves.add((pos[0], pos[1]+1))
    # down:
    if (lower_row & pos_mask_row) | (this_col & pos_mask_col >> 1) == 0:
        valid_moves.add((pos[0]+1, pos[1]))
    # left:
    if (this_row & pos_mask_row << 1) | (left_col & pos_mask_col) == 0:
        valid_moves.add((pos[0], pos[1]-1))
    # up:
    if (upper_row & pos_mask_row) | (this_col & pos_mask_col << 1) == 0:
        valid_moves.add((pos[0]-1, pos[1]))
    
    if log: print(turn, "- current pos:", pos, "can move to:", valid_moves)

    return valid_moves


def bfs(bit_board:BitBoard, start_pos, target_pos):
    # straight forward breadth first search
    start_state = (1, start_pos)
    state_queue = [(None, start_state)]
    seen_states = set()
    index = 0

    while state_queue:

        curr_state = state_queue[index][1]
        curr_turn = curr_state[0]
        curr_pos = curr_state[1]

        prior_state_index = index
        index += 1

        if curr_state in seen_states:
            continue
        seen_states.add(curr_state)

        if curr_pos == target_pos:
            sequence = []
            while prior_state_index is not None:
                prior_state = state_queue[prior_state_index]
                sequence.append(prior_state[1])
                prior_state_index = prior_state[0]
            sequence.reverse()
            return curr_turn, sequence

        for next_pos in get_valid_moves(curr_pos, bit_board, curr_turn, start_pos):
            state_queue.append((prior_state_index, (curr_turn + 1, next_pos)))


#part 1:
start1 = timeit.default_timer()
bitboard1 = BitBoard(clean_data)
ans1, seq1 = bfs(bitboard1, (0,1), (bitboard1.row_count - 2, bitboard1.col_count - 2))
duration1 = timeit.default_timer() - start1
# submit(ans1,1,day,year)

#part 2:
start2 = timeit.default_timer()
# get the board state after part1
bitboard2a = get_new_bit_board_after_waiting(bitboard1, ans1)
# search again with reversed start/end positions
ans2a, seq2a = bfs(bitboard2a, (bitboard1.row_count - 1, bitboard1.col_count - 2), (1,1))
# same idea
bitboard2b = get_new_bit_board_after_waiting(bitboard2a, ans2a)
ans2b, seq2b = bfs(bitboard2b, (0,1), (bitboard1.row_count - 2, bitboard1.col_count - 2))
# add up the minutes for all searches
ans2 = ans1 + ans2a + ans2b
duration2 = timeit.default_timer() - start2
# submit(ans2,2,day,year)

pass