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


def snafu_to_dec(s:str) -> int:
    dec = 0
    for place, digit in enumerate(reversed(s)):
        match digit:
            case '2': dec += 2 * 5 ** place
            case '1': dec += 1 * 5 ** place
            case '-': dec -= 1 * 5 ** place
            case '=': dec -= 2 * 5 ** place
    return dec


def dec_to_snafu(n:int) -> str:
    m, r = divmod(n, 5)
    s = []
    while m > 0 or r > 0:
        if r < 3:
            s.append(str(r))
        if r == 3:
            s.append('=')
            m += 1
        if r == 4:
            s.append('-')
            m += 1
        m, r = divmod(m, 5)
    return ''.join(reversed(s))


def add_snafu_numbers(numbers:str) -> int:
    d = 0
    for s in numbers:
        d += snafu_to_dec(s)
    return dec_to_snafu(d)

#part 1:
start1 = timeit.default_timer()
ans1 = add_snafu_numbers(clean_data)
duration1 = timeit.default_timer() - start1
submit(ans1,1,day,year)

pass