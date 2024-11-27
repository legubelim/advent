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
    return ValueError(f"Invalid delta: {delta}")

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

# part 1
positions = get_positions(get_lines(test=False, testnb=2))

for pos in positions:
    print(f"{pos}")

print(int(len(positions)/2))







