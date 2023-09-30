from aocd.get import get_data
from aocd.post import submit
from ast import literal_eval as leval
import numpy as np
import _utils as util
import os
import re

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")


rock_paths = [[int(item) for item in re.findall(r'\d+(?=[, ]?)', rock)] for rock in clean_data]

abyss_row = 0
for path in rock_paths:
    abyss_row = max(path[1::2] + [abyss_row])

grid = [['.' for i in range(1000)] for i in range(abyss_row+1)]
grid2 = [['.' for i in range(1000)] for i in range(abyss_row+1)]

def draw_line(grid,x1,y1,x2,y2,symbol = '#'):
    grid[y1][x1] = symbol
    grid[y2][x2] = symbol
    if abs(y1-y2) <= 1 and abs(x1-x2) <= 1:
        return
    if y1 == y2:
        for x in range(abs(x2-x1)-1):
            grid[y1][x+min(x1,x2)+1] = symbol
    if x1 == x2:
        for y in range(abs(y2-y1)-1):
            grid[y+min(y1,y2)+1][x1] = symbol

for path in rock_paths:
    for i in range(0,len(path)-2,2):
        draw_line(grid, path[i], path[i+1], path[i+2], path[i+3])
        draw_line(grid2, path[i], path[i+1], path[i+2], path[i+3])

def sand_drop(grid, x=500, y=0, air='.', wall = '#', sand = '+'):
    grid[y][x] = '+'
    still = False
    while still == False:
        if grid[y+1][x] == air:
            grid[y+1][x] = sand
            grid[y][x] = air
            y += 1
            continue
        if grid[y+1][x] == wall or grid[y+1][x] == sand:
            if grid[y+1][x-1] == air:
                grid[y+1][x-1] = sand
                grid[y][x] = air
                y += 1
                x -= 1
                continue
            if grid[y+1][x+1] == air:
                grid[y+1][x+1] = sand
                grid[y][x] = air
                y += 1
                x += 1
                continue

            still = True

ans1 = 0
while '+' not in grid[abyss_row]:
    try:
        sand_drop(grid)
    except:
        break
    ans1 += 1

#part 1:
submit(ans1,1,day,year)

grid2.append(['.' for i in range(1000)])
grid2.append(['#' for i in range(1000)])

ans2 = 0
while grid2[0][500] != '+':
    try:
        sand_drop(grid2)
    except:
        break
    ans2 += 1

#part 2:
submit(ans2,2,day,year)

pass