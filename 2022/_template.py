from aocd.get import get_data
from aocd.post import submit
from ast import literal_eval as leval
from collections import namedtuple
import numpy as np
import polars as pl
import _utils as util
import timeit
import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")

#part 1:
start1 = timeit.default_timer()
duration1 = timeit.default_timer() - start1
#submit(ans1,1,day,year)

#part 2:
start2 = timeit.default_timer()
duration2 = timeit.default_timer() - start2
#submit(ans2,2,day,year)

pass