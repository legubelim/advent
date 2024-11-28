#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import re
import logging
import math

logging.basicConfig(level=logging.DEBUG, format="{message}", style="{")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

##
#%%

def get_lines(test:bool=False, testnb:int=1) -> [str]:
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
        elif testnb == 2:
            string = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

        elif testnb == 3:
            string = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

        elif testnb == 4:
            string = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

        elif testnb == 5:
            string = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

        else:
            raise ValueError("Wrong testnb!")
        lines:[str] = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_10.input', 'r') as file:
            lines:[str] = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

#%%

pipe_types = {
    '|': {'N', 'S'},
    '-': {'E', 'W'},
    'L': {'N', 'E'},
    'J': {'N', 'W'},
    '7': {'S', 'W'},
    'F': {'S', 'E'},
    '.': set()
}

class Coord:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x - other.x, self.y - other.y)

    def __neg__(self) -> 'Coord':
        return Coord(-self.x, -self.y)

    def __eq__(self, other: 'Coord') -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: 'Coord') -> bool:
        return not self.__eq__(other)

    def get_pipe_type(self, lines: [str]) -> str:
        return lines[self.y][self.x]

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Coord({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.__repr__())

    def check_dimensions(self, max_x: int, max_y: int) -> bool:
        return (self.x >= 0) and (self.x <= max_x) and (self.y >= 0) and (self.y <= max_y)



def direction_to_delta(direction: str) -> Coord:
    if direction == 'N': return Coord(0, -1)
    if direction == 'S': return Coord(0, 1)
    if direction == 'E': return Coord(1, 0)
    if direction == 'W': return Coord(-1, 0)
    raise ValueError(f"Unknown direction {direction}!")

def delta_to_direction(delta: Coord) -> str:
    if delta == Coord(0, -1): return 'N'
    if delta == Coord(0, 1): return 'S'
    if delta == Coord(1, 0): return 'E'
    if delta == Coord(-1, 0): return 'W'
    raise ValueError(f"Invalid delta: {delta}")

def next_delta(previous_delta: Coord, pipe_type: str) -> Coord:
    if pipe_type not in pipe_types:
        raise ValueError(f"Unknown pipe type {pipe_type}")
    for direction in pipe_types[pipe_type]:
        delta = direction_to_delta(direction)
        if delta != previous_delta:
            return delta

def find_initial_pos(lines:[str]) -> Coord:
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'S':
                return Coord(x, y)

def find_first_pipe_pos(lines:[str], initial_pos: Coord) -> Coord:
    for direction in ['N', 'S', 'E', 'W']:
        delta = direction_to_delta(direction)
        next_pos = initial_pos + delta
        for direction in pipe_types[next_pos.get_pipe_type(lines)]:
            if delta == -direction_to_delta(direction):
                return next_pos


#lines = get_lines(test=True, testnb=1)
#%%





def get_positions(lines: [str]) -> [Coord]:

    positions:[Coord] = []

    initial_pos = find_initial_pos(lines)
    positions.append(initial_pos)
    print(f"Initial position: {initial_pos}")
    first_pipe_pos = find_first_pipe_pos(lines, initial_pos)
    positions.append(first_pipe_pos)
    print(f"first pipe position: {first_pipe_pos}")

    previous_pos = initial_pos
    pos = first_pipe_pos
    while pos != initial_pos:
        previous_delta = pos - previous_pos
        pipe_type = pos.get_pipe_type(lines)
        for direction in pipe_types[pipe_type]:
            delta = direction_to_delta(direction)
            if delta != -previous_delta:
                break
        previous_pos = pos
        pos = pos + delta
        positions.append(pos)
    return positions
#%%

def print_loop(lines: [str], positions: [Coord], only_loop = True):
    #matrix = []
    for y, line in enumerate(lines):
        row = []
        for x, c in enumerate(line):
            if Coord(x, y) in positions:
                if only_loop: row.append(c)
                else: row.append("0")
            else:
                if only_loop: row.append(" ")
                else: row.append(c)
        row_str = "".join(row)
        #matrix.append(row_str)
        print(row_str)
    #return matrix



#%%

# part 1
lines = get_lines(test=False, testnb=2)
positions = get_positions(lines)

for pos in positions:
    print(f"{pos}")

print(int(len(positions)/2))

#%%

print_loop(lines, positions, only_loop=False)

#%%

# part 2
lines = get_lines(test=False, testnb=2)
positions = get_positions(lines)
del positions[-1]

max_x, max_y = len(lines[0])-1, len(lines)-1
print((max_x, max_y))



#%%
def get_right_deltas(pipe_type: str, direction: str) -> [Coord]:
    if pipe_type == '|':
        if direction == 'N': return [Coord(1,0)]
        elif direction == 'S': return [Coord(-1,0)]
        else: raise ValueError(f"direction {direction} not compatible with pipe type {pipe_type}")
    elif pipe_type == '-':
        if direction == 'E': return [Coord(0,1)]
        elif direction == 'W': return [Coord(0, -1)]
        else: raise ValueError(f"direction {direction} not compatible with pipe type {pipe_type}")
    elif pipe_type == 'L':
        if direction == 'N': return []
        elif direction == 'E': return [Coord(-1, 0), Coord(-1, 1), Coord(0, 1)]
        else: raise ValueError(f"direction {direction} not compatible with pipe type {pipe_type}")
    elif pipe_type == 'J':
        if direction == 'N': return [Coord(0, 1), Coord(1,1), Coord(1, 0)]
        elif direction == 'W': return []
        else: raise ValueError(f"direction {direction} not compatible with pipe type {pipe_type}")
    elif pipe_type == '7':
        if direction == 'W': return [Coord(1, 0), Coord(1, -1), Coord(0, -1)]
        elif direction == 'S': return []
        else: raise ValueError(f"direction {direction} not compatible with pipe type {pipe_type}")
    elif pipe_type == 'F':
        if direction == 'E': return []
        elif direction == 'S': return [Coord(0, -1), Coord(-1, -1), Coord(-1, 0)]
        else: raise ValueError(f"direction {direction} not compatible with pipe type {pipe_type}")
    else:
        raise ValueError(f"invalid pipe type {pipe_type}")


def guess_pipe_type(direction1: str, direction2: str) -> str:
    dir_set = {direction1, direction2}
    if dir_set == {'N', 'S'}: return '|'
    if dir_set == {'W', 'E'}: return '-'
    if dir_set == {'N', 'E'}: return 'L'
    if dir_set == {'N', 'W'}: return 'J'
    if dir_set == {'E', 'S'}: return 'F'
    if dir_set == {'W', 'S'}: return '7'
    raise ValueError(f"invalid direction pair {direction1}, {direction2}")



initial_pipe_type = guess_pipe_type(delta_to_direction(positions[1] - positions[0]),
                               delta_to_direction(positions[0] - positions[-1]))

print(initial_pipe_type)

#%%

positions_set = {c for c in positions}
right_positions_set = set()

for idx, pos in enumerate(positions[:-1]):
    next_idx = (idx + 1) % len(positions)
    delta_pipe = positions[next_idx] - pos
    direction = delta_to_direction(delta_pipe)
    pipe_type = pos.get_pipe_type(lines) if idx != 0 else initial_pipe_type
    for delta in get_right_deltas(pipe_type, direction):
        right_pos = pos + delta
        if (right_pos not in positions_set) and right_pos.check_dimensions(max_x, max_y):
            right_positions_set.add(right_pos)


print_loop(lines, list(right_positions_set), only_loop=True)


