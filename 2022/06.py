from aocd.get import get_data
from aocd.post import submit
day = 6
year = 2022
data = get_data(day=day, year=year)
print(data)

def first_distinct_substring(str, substr_len):
    for char in range(len(str)):
        if char < substr_len-1:
            pass
        if len(set(str[char-substr_len:char])) == substr_len:
            return char

ans1 = first_distinct_substring(data, 4)

#part 1:
submit(ans1,1,day,year)

ans2 = first_distinct_substring(data, 14)

#part 2:
submit(ans2,2,day,year)

pass