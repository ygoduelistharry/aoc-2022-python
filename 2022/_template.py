from aocd.get import get_data
from aocd.post import submit
import numpy as np
day = 1
year = 2022
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

#part 1:
#submit(ans1,1,day,year)

#part 2:
#submit(ans2,2,day,year)

pass