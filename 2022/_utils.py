'''Utility functions I've found useful'''
import os

def char_to_index(char:str):
    if char.isdigit():
        return int(char)
    if ord(char)>=97:
        return ord(char) - 96
    if ord(char)>=65:
        return ord(char) - 38

def get_file_name(file = __file__):
    '''Returns current file name without an extension (usually .py)'''
    return os.path.splitext(os.path.basename(file))[0]

def custom_bubble_sort(arr:list, comparator=None):
    '''Sorts an array by result of comparator function. Function 'comparator' must compare objects a & b and return True if a < b for purposes of sort. If none specified, a normal less than function is used. Mutates in place.'''

    if comparator is None:
        def lte(l,r):
            return l <= r
        comparator = lte

    n = len(arr)

    for i in range(n):
        for j in range(n-i-1):
            left = arr[j]
            right = arr[j+1]
            if comparator(left, right):
                continue
            else:
                arr[j] = right
                arr[j+1] = left

# Useful regex strings:
re_get_ints = r'-?\d+'