from aocd.get import get_data
from aocd.post import submit
day = 8
year = 2022
data = get_data(day=day, year=year)
print(data)

tree_grid = data.split("\n")
rows = len(tree_grid)
cols = len(tree_grid[0])
for row in range(rows):
    tree_grid[row] = [int(char) for char in tree_grid[row]]

n_map = [[0 for tree in r] for r in tree_grid]
s_map = [[0 for tree in r] for r in tree_grid]
e_map = [[0 for tree in r] for r in tree_grid]
w_map = [[0 for tree in r] for r in tree_grid]
vis_map = [[0 for tree in r] for r in tree_grid]

for row in range(rows):
    n_row = row
    s_row = rows-row-1
    for col in range(cols):
        w_col = col
        e_col = cols-col-1
        n_h = tree_grid[n_row][col]
        s_h = tree_grid[s_row][col]
        w_h = tree_grid[row][w_col]
        e_h = tree_grid[row][e_col]

        if n_row == 0:
            n_map[n_row][col] = n_h
        else:
            n_map[n_row][col] = max(n_h,n_map[n_row-1][col])

        if s_row == rows-1:
            s_map[s_row][col] = s_h
        else:
            s_map[s_row][col] = max(s_h,s_map[s_row+1][col])

        if w_col == 0:
            w_map[row][w_col] = w_h
        else:
            w_map[row][w_col] = max(w_h,w_map[row][w_col-1])

        if e_col == cols-1:
            e_map[row][e_col] = e_h
        else:
            e_map[row][e_col] = max(e_h,e_map[row][e_col+1])

def check_visibility(tree_grid,n,s,e,w,row,col):
    rows = len(tree_grid)
    cols = len(tree_grid[0])

    if row == 0 or row == rows-1 or col == 0 or col == cols-1:
        return True

    height = tree_grid[row][col]
    if height > min(n[row-1][col], s[row+1][col], e[row][col+1], w[row][col-1]):
        return True
    
    return False


for row in range(rows):
    for col in range(cols):
        if check_visibility(tree_grid, n_map, s_map, e_map, w_map, row, col) is True:
            vis_map[row][col] = 1
        else:
            vis_map[row][col] = 0
        
ans1 = sum([sum(row) for row in vis_map])

#part 1:
submit(ans1,1,day,year)

def calc_scenic_score(tree_grid,row,col):
    rows = len(tree_grid)
    cols = len(tree_grid[0])
    height = tree_grid[row][col]

    if row == 0 or col == 0 or row == rows-1 or col == cols-1:
        return 0
    
    r_vis = 0
    d_vis = 0
    l_vis = 0
    u_vis = 0

    #check right
    for i in range(col+1,cols):
        if height > tree_grid[row][i]:
            r_vis += 1
        if height == tree_grid[row][i]:
            r_vis += 1
            break
    
    #check down
    for i in range(row+1,rows):
        if height > tree_grid[i][col]:
            d_vis += 1
        if height == tree_grid[i][col]:
            d_vis += 1
            break
    
    #check left
    for i in range(0,col):
        if height > tree_grid[row][col-i-1]:
            l_vis += 1
        if height == tree_grid[row][col-i-1]:
            l_vis += 1
            break
    
    #check up
    for i in range(0,row):
        if height > tree_grid[row-i-1][col]:
            u_vis += 1
        if height == tree_grid[row-i-1][col]:
            u_vis += 1
            break

    return r_vis*d_vis*l_vis*u_vis

ans2 = 0

for row in range(rows):
    for col in range(cols):
        s = calc_scenic_score(tree_grid,row,col)
        if s > ans2:
            ans2 = s

#part 2:
submit(ans2,2,day,year)

pass