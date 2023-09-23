from aocd.get import get_data
from aocd.post import submit
import numpy as np
import _utils as u

day = 12
year = 2022
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

grid = np.array([[u.char_to_index(col) for col in row] for row in clean_data])

finish = (20,43)
grid[20][43] = 26
start = (20,0)
grid[20][0] = 1

def in_2D_array_range(_2D_array,pos):
    r = pos[0]
    c = pos[1]
    r_max = _2D_array.shape[0]
    c_max = _2D_array.shape[1]
    return r >= 0 and c >= 0 and r < r_max and c < c_max

def djikstra(grid,start,finish):
    try:
        grid[start[0]][start[1]]
        grid[finish[0]][finish[1]]       
    except:
        return print("Start or finish not in bounds")

    path_grid = np.zeros(grid.shape, dtype=int)
    finish = np.array(finish, dtype=int)
    cur_frontier = np.array([start], dtype=int)
    new_frontier = np.array([start], dtype=int)
    visited = np.array([start], dtype=int)
    u_vecs = [
        [0,1],
        [1,0],
        [0,-1],
        [-1,0]
    ]
    path_len = 0

    while finish.tolist() not in new_frontier.tolist():
        new_frontier = np.array([], dtype=int)
        for pos in cur_frontier:
            adj = np.array([pos+d for d in u_vecs], dtype=int)
            valid = []
            for new_pos in adj:
                if not in_2D_array_range(grid,new_pos):
                    continue
                if new_pos.tolist() in visited.tolist():
                    continue
                if new_pos.tolist() in new_frontier.tolist():
                    continue
                if grid[new_pos[0]][new_pos[1]] - grid[int(pos[0])][int(pos[1])] < -1:
                    continue
                valid.append(new_pos)
                path_grid[new_pos[0]][new_pos[1]] = path_len+1

            new_frontier = np.append(new_frontier, valid).reshape(-1,2)
            visited = np.append(visited, valid).reshape(-1,2)
        path_len += 1
        cur_frontier = new_frontier.copy()
        if path_len > 1000:
            break
    
    return path_len, path_grid


ans1, path_grid = djikstra(grid,finish,start)

#part 1:
submit(ans1,1,day,year)

flat_grid = grid.reshape(-1)
flat_path_grid = path_grid.reshape(-1)
lens = [v for k, v in enumerate(flat_path_grid) if flat_grid[k] == 1 and v != 0]
ans2 = int(min(lens))

#part 2:
submit(ans2,2,day,year)
pass