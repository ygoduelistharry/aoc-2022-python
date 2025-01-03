from aocd.get import get_data
from aocd.post import submit
import _utils as util
import timeit
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")
map = clean_data

# we can store all the starting elf positions as a set of vectors
starting_positions:dict[tuple[int,int],list[int]] = {}
# we also need to store an id for each elf
id = 0
for row in range(len(map)):
    for col in range(len(map[row])):
        if map[row][col] == '#':
            starting_positions.update({(row,col):[id]})
            id += 1

#assigning adjacent vectors a bitmask
adj_vec_mask = {
    (0,1)  :2**0, #E
    (1,1)  :2**1, #SE
    (1,0)  :2**2, #S
    (1,-1) :2**3, #SW
    (0,-1) :2**4, #W
    (-1,-1):2**5, #NW
    (-1,0) :2**6, #N
    (-1,1) :2**7, #NE
}

#assigning the cardinal directions to a direction vector
dir_i2vec = {
    0:(-1,0), #N
    1:(1,0) , #S
    2:(0,-1), #W
    3:(0,1) , #E
}

#assigning the cardinal directions to the 3 tile bitmask that needs to be empty to move
dir_mask = {
    0: 2**7 + 2**6 + 2**5, #N
    1: 2**3 + 2**2 + 2**1, #S
    2: 2**5 + 2**4 + 2**3, #W
    3: 2**7 + 2**1 + 2**0, #E
}

def process_rounds(starting_positions:dict[tuple[int,int],list[int]], rounds = None) -> dict:
    
    current_positions = starting_positions.copy()
    round = 0

    # if rounds == None, then it will just iterate until the elves stop moving
    while rounds == None or round < rounds:
        # step 1: propose movements
        
        # mapping of proposed positions to list of elf ids trying to get there
        proposed_positions:dict[tuple[int,int],list[int]] = {}
        # mapping of elf ids to their current (soon to be old) positions
        old_positions:dict[int,tuple[int,int]] = {}
        # which direction elves will prioritise moving to this round
        priority_dir_id = round % 4

        for pos, id in current_positions.items():
            id = id.copy()
            adjacent_elves = 0
            # for each adjacent tile, if there is an elf there we add the mask for that tile
            for rel, val in adj_vec_mask.items():
                check_pos = (pos[0]+rel[0], pos[1]+rel[1])
                if check_pos in current_positions:
                    adjacent_elves += val
            
            # if we didnt add anything, there are no adjacent elves
            if adjacent_elves == 0:
                # so the proposed move is the current position
                proposed_positions.update({pos:id})
                # and we can move to the next elf
                continue

            # store the current position in case we collide and need to go back
            old_positions.update({id[0]: pos})
            # check all 4 cardinal directions
            for d in range(4):
                # starting with the current priority direction
                dir_id = (priority_dir_id + d) % 4
                # get the 3 tile bit mask for this direction
                comparand = dir_mask[dir_id]
                # and compare to the adjacent elves mask
                # if empty we add it to the proposed positions
                # and track what ids have proposed this position
                if adjacent_elves & comparand == 0:
                    rel = dir_i2vec[dir_id]
                    proposed_pos = (pos[0]+rel[0], pos[1]+rel[1])
                    if proposed_pos in proposed_positions:
                        proposed_positions[proposed_pos].extend(id)
                    else:
                        proposed_positions.update({proposed_pos:id})
                    move_proposed = True
                    break
                # if every direction was blocked in some way then we dont move
                move_proposed = False
            
            # and the proposed position is the current position
            if not move_proposed:
                proposed_positions.update({pos:id})

        # if the proposed positions are the same as the current positions
        if proposed_positions.keys() == current_positions.keys():
            round += 1
            # we reached steady state and we are done!
            break

        # step 2: process movements
        next_positions:dict[tuple[int,int],list[int]] = {}

        # for each proposed position
        for pos, id in proposed_positions.items():
            id = id.copy()
            # if there is only 1 elf that proposed the position, there was no collision
            if len(id) == 1:
                # and the elf can move
                next_positions.update({pos:id})
            # if not, there will be a collision
            else:
                # so the next position of these elves will be their current position
                for elf_id in id:
                    old_pos = old_positions[elf_id]
                    next_positions.update({old_pos:[elf_id]})
        
        current_positions = next_positions
        round += 1

    return current_positions, round


def get_empty_tiles(positions:set[tuple[int,int]]) -> int:
    occupied_tiles = len(positions)
    row_values = {p[0] for p in positions}
    col_values = {p[1] for p in positions}
    
    area = (max(row_values) - min(row_values) + 1) * (max(col_values) - min(col_values) + 1)
    return area - occupied_tiles


#part 1:
start1 = timeit.default_timer()
positions1, _ = process_rounds(starting_positions, 10)
ans1 = get_empty_tiles(positions1.keys())
duration1 = timeit.default_timer() - start1
#submit(ans1,2,day,year)

#part 2:
start2 = timeit.default_timer()
_, ans2 = process_rounds(starting_positions)
duration2 = timeit.default_timer() - start2
#submit(ans2,2,day,year)

pass