from aocd.get import get_data
from aocd.post import submit
from ast import literal_eval as leval
import numpy as np
import _utils as util
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

#recursion
def compare_nested_lists(left, right):

    if isinstance(left,int) and isinstance(right,int):
        if left != right:
            return left < right

    if isinstance(left,int):
        left = [left]

    if isinstance(right,int):
        right = [right]

    if len(left) == 0 and len(right) > 0:
        return True
    
    if len(left) > 0 and len(right) == 0:
        return False
        
    for i in range(max(len(left),len(right))):

        if i > len(left) - 1:
            return True
        if i > len(right) - 1:
            return False
        if left[i] == right[i]:
            continue

        return compare_nested_lists(left[i], right[i])

ans1 = 0
for a in range(0,len(clean_data),3):
    left = leval(clean_data[a])
    right = leval(clean_data[a+1])
    if compare_nested_lists(left,right):
        ans1 += a/3 + 1

ans1 = int(ans1)

#part 1:
submit(ans1,1,day,year)

clean_data2 = [leval(i) for i in clean_data if i != '']
clean_data2.extend([[[2]],[[6]]])

util.custom_bubble_sort(clean_data2, compare_nested_lists)

ans2 = (clean_data2.index([[2]])+1)*(clean_data2.index([[6]])+1)

#part 2:
submit(ans2,2,day,year)

pass