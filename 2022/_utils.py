'''Utility functions I've found useful'''

def char_to_index(char:str):
    if char.isdigit():
        return int(char)
    if ord(char)>=97:
        return ord(char) - 96
    if ord(char)>=65:
        return ord(char) - 38