#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
from collections.abc import Iterable
from typing import Optional

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
            string = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

        else:
            raise ValueError("Wrong testnb!")
        lines:[str] = string.splitlines()

    else:
        # getting lines from input file
        with open('2023/day_14.input', 'r') as file:
            lines:[str] = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

#%%


def tilt_row(row_in: [str], reverse=False) -> [str]:
    if reverse:
        row = list(reversed(row_in))
    else:
        row = row_in.copy()
    for i in range(len(row)-1, -1, -1):
        c = row[i]
        if c == 'O':
            dest = i
            for i_to in range(i+1, len(row)):
                if row[i_to] != '.':
                    break
                else:
                    dest = i_to
            if dest != i:
                row[dest] = 'O'
                row[i] = '.'
    if reverse:
        row = list(reversed(row))
    return row

#%%

def transpose(matrix: list[list[str]]) -> list[list[str]]:
    matrix_out = []
    for x in range(0, len(matrix[0])):
        out_row = [row[x] for row in matrix]
        matrix_out.append(out_row)
    return matrix_out

def tilt(matrix_in: [[str]], direction:str='N') -> [[str]]:
    if direction == 'S':
        matrix = transpose(matrix_in)
        reverse = False
    elif direction == 'N':
        matrix = transpose(matrix_in)
        reverse = True
    elif direction == 'W':
        matrix = matrix_in
        reverse = True
    elif direction == 'E':
        matrix = matrix_in
        reverse = False
    else:
        raise ValueError(f"invalid direction {direction}")

    matrix_out = []
    for row in matrix:
        row_out = tilt_row(row, reverse)
        matrix_out.append(row_out)

    if (direction == 'S') or (direction == 'N'):
        return transpose(matrix_out)
    else:
        return matrix_out

def compute_matrix_load(matrix_in: [[str]]) -> int:
    load = 0
    matrix = transpose(matrix_in)
    dim_y = len(matrix[0])
    for row in matrix:
        for y, c in enumerate(row):
            if c == 'O':
                load += dim_y - y
    return load


#%%
def print_matrix(matrix: [[str]]):
    for r in matrix:
        print(r)

#%%

# part 1
matrix = get_lines(test=True, testnb=1)
print(compute_matrix_load(tilt(matrix, 'N')))

#%%

matrix = get_lines(test=False, testnb=1)
print(compute_matrix_load(tilt(matrix, 'N')))

#%%

def run_cycle(matrix: [[str]]) -> [[str]]:
    matrix = tilt(matrix, 'N')
    matrix = tilt(matrix, 'W')
    matrix = tilt(matrix, 'S')
    matrix = tilt(matrix, 'E')
    return matrix

matrix = get_lines(test=False, testnb=1)

hashes = {}
for i in range(1, 1000000000+1):
    if i % 100000 == 0:
        print(f"-- cycle nb : {i}")
    matrix = run_cycle(matrix)
    matrix_str = "".join(["".join(row) for row in matrix])
    h = hash(matrix_str)
    if h in hashes:
        cycle_start, cycle_length = hashes[h], i - hashes[h]
        print(f"cycle detected between {cycle_start} and {i}")
        print(f"cycle length: {cycle_length}")
        break
    else:
        hashes[h] = i

cycles_to_run = (1000000000 - cycle_start) % cycle_length # we already ran cycle_start cycles
print(f"cycles to run: {cycles_to_run}")
for _ in range(0, cycles_to_run):
    matrix = run_cycle(matrix)

print(f"load: {compute_matrix_load(matrix)}")

