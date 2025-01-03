from aocd.get import get_data
from aocd.post import submit
from collections import deque
import _utils as util
import timeit
import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")
example_data =[
'        ...#',
'        .#..',
'        #...',
'        ....',
'...#.......#',
'........#...',
'..#....#....',
'..........#.',
'        ...#....',
'        .....#..',
'        .#......',
'        ......#.',
'10R5L5R10L4R5L5',
]

example_map = example_data[0:12]
example_instructions = example_data[-1]

map = clean_data[0:200]
instructions = clean_data[-1]


def process_instructions1(map, instructions) -> tuple[int,int,int]:
    # part 1 instuction processing
    current_row = 0
    current_col = map[0].index('.')
    current_facing = 0 #right
    movements = deque([int(m) for m in re.findall(util.re_get_ints, instructions)])
    rotations = deque(re.findall(r'[A-Z]', instructions))

    while movements or rotations:
        current_row_map = map[current_row]
        if movements:
            move_dist = movements.popleft()
            match current_facing:

                case 0: #right
                    target_col = current_col
                    for _ in range(move_dist):
                        target_col += 1
                        if target_col >= len(current_row_map) or current_row_map[target_col] == ' ':
                            target_col = min(current_row_map.index('.'), current_row_map.index('#'))
                        if current_row_map[target_col] == '#':
                            break
                        current_col = target_col
                case 2: #left
                    target_col = current_col
                    for _ in range(move_dist):
                        target_col -= 1
                        if target_col < 0 or current_row_map[target_col] == ' ':
                            target_col = len(current_row_map) - 1
                        if current_row_map[target_col] == '#':
                            break
                        current_col = target_col    
                case 1: #down
                    target_row = current_row
                    for _ in range(move_dist):
                        target_row += 1
                        if target_row >= len(map) or len(map[target_row]) <= current_col or map[target_row][current_col] == ' ':
                            target_row = 0
                        while len(map[target_row]) <= current_col or map[target_row][current_col] == ' ':
                            target_row += 1
                        if map[target_row][current_col] == '#':
                            break
                        current_row = target_row
                case 3: #up
                    target_row = current_row
                    for _ in range(move_dist):
                        target_row -= 1
                        if target_row < 0 or len(map[target_row]) <= current_col or map[target_row][current_col] == ' ':
                            target_row = len(map) - 1
                        while len(map[target_row]) <= current_col or map[target_row][current_col] == ' ':
                            target_row -= 1
                        if map[target_row][current_col] == '#':
                            break
                        current_row = target_row

        if rotations:
            rotation = rotations.popleft()
            if rotation == 'L':
                current_facing = (current_facing - 1) % 4
            if rotation == 'R':
                current_facing = (current_facing + 1) % 4

    return (current_row, current_col, current_facing)


def cubify(map, size=50) -> list[list[str]]:
    # turns an unfolded cube puzzle input map into a list of 6 square maps of size
    # returned in 'book reading' order (left to right, top to bottom)
    # for my unfolding, the returned list of faces [0,1,2,3,4,5] corresponds to:
    #
    #   _ 0 1
    #   _ 2 _
    #   3 4 _
    #   5 _ _
    #

    faces = []
    for y in range(int(len(map)/size)):
        row = y*size
        for x in range(int(len(map[row])/size)):
            col = x*size
            if map[row][col] == ' ':
                continue
            face = []
            for r in range(size):
                face.append(map[row+r][col:col+size])
            faces.append(face.copy())
    return faces


def edge_mapping(face, row, col, dir, size=50) -> tuple[int,int,int,int]:
    # returns where you will end up (local) and in which direction you will be facing (global) when walking off the edge of a cube face
    # specific to my puzzle input unfolding (seems way too hard to generalise)
    max = size - 1
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    match face, dir:
        case 0, 0: target = (1, row, 0, RIGHT)
        case 0, 1: target = (2, 0, col, DOWN)
        case 0, 2: target = (3, max - row, 0, RIGHT)
        case 0, 3: target = (5, col, 0, RIGHT)

        case 1, 0: target = (4, max - row, max, LEFT)
        case 1, 1: target = (2, col, max, LEFT)
        case 1, 2: target = (0, row, max, LEFT)
        case 1, 3: target = (5, max, col, UP)

        case 2, 0: target = (1, max, row, UP)
        case 2, 1: target = (4, 0, col, DOWN)
        case 2, 2: target = (3, 0, row, DOWN)
        case 2, 3: target = (0, max, col, UP)

        case 3, 0: target = (4, row, 0, RIGHT)
        case 3, 1: target = (5, 0, col, DOWN)
        case 3, 2: target = (0, max - row, 0, RIGHT)
        case 3, 3: target = (2, col, 0, RIGHT)

        case 4, 0: target = (1, max - row, max, LEFT)
        case 4, 1: target = (5, col, max, LEFT)
        case 4, 2: target = (3, row, max, LEFT)
        case 4, 3: target = (2, max, col, UP)

        case 5, 0: target = (4, max, row, UP)
        case 5, 1: target = (1, 0, col, DOWN)
        case 5, 2: target = (0, 0, row, DOWN)
        case 5, 3: target = (3, max, col, UP)

    return target



def process_instructions2(maps:list[list[str]], instructions:str) -> tuple[int,int,int]:
    # starting position
    c_face = 0
    c_row = 0
    c_col = 0
    c_dir = 0 #right
    movements = deque([int(m) for m in re.findall(util.re_get_ints, instructions)])
    rotations = deque(re.findall(r'[A-Z]', instructions))

    while movements or rotations:
        if movements:
            move_dist = movements.popleft()
            for _ in range(move_dist):
                # check the direction we are facing
                match c_dir:
                    case 0: #right
                        # update target position on current face (in this case, 1 square to the right)
                        (t_row, t_col) = (c_row, c_col + 1)
                        # check if we are going to walk off an edge and set a flag for later
                        if t_col >= len(maps[c_face][c_row]): walk_off = True
                        else: walk_off = False
                    
                    # other cases are the same but check a different map edge
                    case 1: #down
                        (t_row, t_col) = (c_row + 1, c_col)
                        if t_row >= len(maps[c_face]): walk_off = True
                        else: walk_off = False

                    case 2: #left
                        (t_row, t_col) = (c_row, c_col - 1)
                        if t_col < 0: walk_off = True
                        else: walk_off = False

                    case 3: #up
                        (t_row, t_col) = (c_row - 1, c_col)
                        if t_row < 0: walk_off = True
                        else: walk_off = False

                # if we are going to walk off a cube face use the edge mapping function to find where we would end up
                if walk_off:    (t_face, t_row, t_col, t_dir) = edge_mapping(c_face, c_row, c_col, c_dir)
                # otherwise just stay on the current face
                else:           (t_face, t_dir) = (c_face, c_dir)
                # if target position is a wall, finish processing this movement and DON'T update our current position
                if maps[t_face][t_row][t_col] == '#': break
                # otherwise, update our current position and direction and try to move again
                (c_face, c_row, c_col, c_dir) = (t_face, t_row, t_col, t_dir)

        # deal with the rotation
        if rotations:
            rotation = rotations.popleft()
            if rotation == 'L':
                c_dir = (c_dir - 1) % 4
            if rotation == 'R':
                c_dir = (c_dir + 1) % 4

    # return the final cube face and local position
    return (c_face, c_row, c_col, c_dir)



def local_pos_to_global(face:int, row:int, col:int, dir:int, size=50) -> tuple[int,int,int]:
    # maps the local cube face position to the global unfolded map position
    match face:
        case 0: return (row         , col+size  , dir)
        case 1: return (row         , col+2*size, dir)
        case 2: return (row+size    , col+size  , dir)
        case 3: return (row+2*size  , col       , dir)
        case 4: return (row+2*size  , col+size  , dir)
        case 5: return (row+3*size  , col       , dir)



def get_password(row, col, dir) -> int:
    return (row + 1) * 1000 + (col + 1) * 4 + dir



#part 1:
start1 = timeit.default_timer()
endpoint1 = process_instructions1(map, instructions)
ans1 = get_password(*endpoint1)
duration1 = timeit.default_timer() - start1
# submit(ans1,1,day,year)


#part 2:
start1 = timeit.default_timer()
cube_face_maps = cubify(map,50)
local_endpoint2 = process_instructions2(cube_face_maps, instructions)
endpoint2 = local_pos_to_global(*local_endpoint2)
ans2 = get_password(*endpoint2)
duration2 = timeit.default_timer() - start1
# submit(ans2,2,day,year)

pass