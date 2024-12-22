from aocd.get import get_data
from aocd.post import submit
from collections import namedtuple
import _utils as util
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")


#part 1:
Point = namedtuple('Point',['x','y','z'])
lava_points = {Point(*map(int, p.split(","))) for p in clean_data}

def get_adjacent_points(p:Point) -> list[Point]:
    xya = Point(p.x, p.y, p.z + 1)
    xyb = Point(p.x, p.y, p.z - 1)
    xza = Point(p.x, p.y + 1, p.z)
    xzb = Point(p.x, p.y - 1, p.z)
    yza = Point(p.x + 1, p.y, p.z)
    yzb = Point(p.x - 1, p.y, p.z)
    return [xya, xyb, xza, xzb, yza, yzb]

adjacent_point_cache = {}
surface_area = 0
for p in lava_points:
    surface_area += 6
    if p in adjacent_point_cache:
        surface_area -= 2 * adjacent_point_cache[p]
    for adjacent_point in get_adjacent_points(p):
        if adjacent_point in adjacent_point_cache:
            adjacent_point_cache[adjacent_point] += 1
        else:
            adjacent_point_cache[adjacent_point] = 1
    
ans1 = surface_area
# submit(ans1,1,day,year)

#part 2:
# do a breadth first search starting from the corner of a box containing ALL of the lava
start_point = Point(
    min(lava_points, key=lambda p:p.x).x - 1,
    min(lava_points, key=lambda p:p.y).y - 1,
    min(lava_points, key=lambda p:p.z).z - 1,
) 
end_point = Point(
    max(lava_points, key=lambda p:p.x).x + 1,
    max(lava_points, key=lambda p:p.y).y + 1,
    max(lava_points, key=lambda p:p.z).z + 1,
)

def point_is_out_of_bounds(p:Point):
    for axis, value in enumerate(p):
        if value > end_point[axis] or value < start_point[axis]:
            return True
    return False

point_queue = [start_point]
points_queued = set()
points_visited = set()
index = 0
exterior_surface_area = 0

while index < len(point_queue):
    print(index)
    current_point = point_queue[index]
    if current_point in adjacent_point_cache:
        exterior_surface_area += adjacent_point_cache[current_point]
    points_visited.add(current_point)
    for point in get_adjacent_points(current_point):
        if (point in points_visited
            or point in points_queued
            or point in lava_points
            or point_is_out_of_bounds(point)
            ):
            continue
        else:
            point_queue.append(point)
            points_queued.add(point)
    index += 1


ans2 = exterior_surface_area
submit(ans2,2,day,year)

pass