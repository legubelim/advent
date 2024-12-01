#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
from collections.abc import Iterable

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
            string = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

        else:
            raise ValueError("Wrong testnb!")
        lines:[str] = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_11.input', 'r') as file:
            lines:[str] = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

#%%

# part 1

def expand_universe(lines: [str]) -> [str]:
    matrix = []
    dim_x, dim_y = len(lines[0]), len(lines)
    for line in lines:
        row = [c for c in line]
        matrix.append(row)
        if '#' not in row:
            matrix.append(row.copy())
    shift = 0
    for x in range(0, dim_x):
        column = [lines[y][x] for y in range(0, dim_y)]
        if '#' not in column:
            for y in range(0, len(matrix)):
                matrix[y].insert(x + shift, '.')
            shift += 1
    universe = ["".join(row) for row in matrix]
    return universe

universe = expand_universe(get_lines(test=False))
for row in universe:
    logger.debug(row)

#%%

def find_galaxies(universe: [str]) -> Iterable[tuple[int, int]]:
    dim_x, dim_y = len(universe[0]), len(universe)
    galaxies = []
    for y in range(0, dim_y):
        for x in range(0, dim_x):
            if universe[y][x] == '#':
                galaxies.append((x, y))
    return galaxies

galaxies = find_galaxies(universe)
logger.debug(galaxies)

#%%

result = 0
for idx, origin in enumerate(galaxies):
    for destination in galaxies[idx+1:]:
        result += abs(destination[0] - origin[0]) + abs(destination[1] - origin[1])

print(result)

#%%

def get_universe_expansions(lines: [str]) -> tuple[Iterable[int], Iterable[int]]:
    exp_xs, exp_ys = [], []
    dim_x, dim_y = len(lines[0]), len(lines)
    matrix = []
    for y, line in enumerate(lines):
        row = [c for c in line]
        matrix.append(row)
        if '#' not in row:
            exp_ys.append(y)
    for x in range(0, dim_x):
        column = [lines[y][x] for y in range(0, dim_y)]
        if '#' not in column:
            exp_xs.append(x)
    return exp_xs, exp_ys

lines = get_lines(test=False)
exp_xs, exp_ys = get_universe_expansions(lines)

logger.debug(f"columns to expand: x in {exp_xs}")
logger.debug(f"rows    to expand: y in {exp_ys}")

galaxies = find_galaxies(lines)
logger.debug(galaxies)

exp_rate = 1000000

def is_between(nb: int, limita: int, limitb: int) -> bool:
    return (limita <= nb <= limitb) or (limita >= nb >= limitb)

result = 0
for idx, origin in enumerate(galaxies):
    (origin_x, origin_y) = origin
    for destination in galaxies[idx+1:]:
        trace = True if origin == (9, 6) and destination == (7, 8) else False
        if trace:
            print(f"origin: {origin} destination: {destination}")
        destination_x, destination_y = destination
        result += abs(destination_x - origin_x) + abs(destination_y - origin_y)
        if trace: print(f"initial distance: {abs(destination_x - origin_x) + abs(destination_y - origin_y)}")
        for x in exp_xs:
            if is_between(x, origin_x, destination_x):
                if trace: print(f"expansion for x = {x} adding {exp_rate - 1}")
                result += exp_rate - 1
        for y in exp_ys:
            if is_between(y, origin_y, destination_y):
                if trace: print(f"expansion for y = {y} adding {exp_rate - 1}")
                result += exp_rate - 1


print(result)

