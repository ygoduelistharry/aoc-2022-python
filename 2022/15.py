from aocd.get import get_data
from aocd.post import submit
import _utils as util
import itertools
import os
import re

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")
num_data = [re.findall(util.re_get_ints, s) for s in clean_data]

#part 1:
def mdist(x1,y1,x2,y2): return abs(int(x1)-int(x2)) + abs(int(y1)-int(y2))

class Sensor():
    def __init__(self, sx, sy, bx, by):
        self.sx = int(sx)
        self.sy = int(sy)
        self.bx = int(bx)
        self.by = int(by)
        self.md = mdist(self.sx,self.sy,self.bx,self.by)

    def contains(self,x,y):
        if mdist(self.sx,self.sy,x,y) > self.md: return False
        else: return True
    
    def x_bounds(self, y): # bounds are left inclusive, right exclusive
        if abs(self.sy - y) > self.md: return None
        else: return [
            ('L',self.sx - (self.md - abs(y-self.sy))),
            ('R',self.sx + (self.md - abs(y-self.sy) + 1)),
        ]


def h_scan_bounds(y:int, sensor_data:list[Sensor]):
    all_x_bounds = [s.x_bounds(y) for s in sensor_data if s.x_bounds(y) is not None]
    all_x_bounds = list(itertools.chain(*all_x_bounds))
    all_x_bounds = sorted(all_x_bounds, key = lambda x: x[1])
    assert all_x_bounds[0][0] == 'L' and all_x_bounds[-1][0] == 'R'
    inbound_count = 0
    bounds = []
    for b in all_x_bounds:
        lr = b[0]
        x = b[1]
        if lr == 'L':
            if inbound_count == 0:
                bounds.append((lr,x))
            if inbound_count >= 0: inbound_count += 1
        if lr == 'R':
            if inbound_count > 0: inbound_count -= 1
            if inbound_count == 0:
                bounds.append((lr,x))
    assert len(bounds)%2 == 0
    return bounds
    
def h_scan_count_inbound_points(y:int, sensor_data:list[Sensor]):
    bounds = h_scan_bounds(y, sensor_data)
    count_points = 0
    for b in bounds:
        if b[0] == 'L': in_x = b[1]
        if b[0] == 'R':
            out_x = b[1]
            count_points += out_x - in_x
    return count_points

y = 2000000
sensor_list = [Sensor(*s) for s in num_data]
beacon_list = {(s.bx,s.by) for s in sensor_list}
bounds = h_scan_bounds(1000000, sensor_list)
ans1 = h_scan_count_inbound_points(y, sensor_list) - len({b for b in beacon_list if b[1] == y})

submit(ans1,1,day,year)

#part 2:
# missing beacon will be JUST outside of range:
# find the point on sensor outer edge that ISN'T in another sensors range
min = 0
max = 4000000

def is_missing_beacon(x,y):
    if x < min or y < min or x > max or y > max:
        return False
    for s in sensor_list:
        if s.contains(x,y): return False
    return True

# find equations of lines that define outer edges (they will be or form y = x + c OR y = -x + c)
# the missing beacon will be at the intersection of duplicated bounds

def get_outer_edge_equations(sensor:Sensor) -> list[tuple[int,int]]:
    outer_w_point = sensor.sx - sensor.md - 1
    outer_e_point = sensor.sx + sensor.md + 1
    # c = y - m*x where m = 1 or -1
    nw_eq = (1, sensor.sy - 1 * outer_w_point)
    sw_eq = (-1, sensor.sy + 1 * outer_w_point)
    ne_eq = (-1, sensor.sy + 1 * outer_e_point)
    se_eq = (1, sensor.sy - 1 * outer_e_point)
    return [nw_eq, sw_eq, ne_eq, se_eq]

edge_equation_dict = {}

for s in sensor_list:
    for eq in get_outer_edge_equations(s):
        if eq in edge_equation_dict:
            edge_equation_dict[eq] += 1
        else:
            edge_equation_dict[eq] = 1

def find_linear_eq_intersect(eq1, eq2):
    m1 = eq1[0]
    m2 = eq2[0]
    c1 = eq1[1]
    c2 = eq2[1]
    x = (c2 - c1)/(m1 - m2)
    y = m1 * x + c1
    return (x, y)

duplicate_pos_eqs = {k for k, v in edge_equation_dict.items() if v > 1 and k[0] == 1}
duplicate_neq_eqs = {k for k, v in edge_equation_dict.items() if v > 1 and k[0] == -1}

for neq in duplicate_neq_eqs:
    for peq in duplicate_pos_eqs:
        (x, y) = find_linear_eq_intersect(neq, peq)
        if is_missing_beacon(x, y):
            ans2 = int(max * x + y)
            break

submit(ans2,2,day,year)

