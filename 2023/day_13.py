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
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

        else:
            raise ValueError("Wrong testnb!")
        lines:[str] = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_13.input', 'r') as file:
            lines:[str] = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

#%%

def read_lines(lines: [str]) -> Iterable[list[str]]:
    patterns = []
    pattern = []
    for line in lines:
        if line == "":
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns

patterns = read_lines(get_lines(test=True, testnb=1))
for pattern in patterns:
    logger.debug(pattern)

#%%

def find_refl1(rows: list[str]) -> Optional[int]:
    for i, row in enumerate(rows[:-1]):
        if rows[i] == rows[i+1]:
            max_refl = min(i, len(rows)-1 - (i+1))
            refl = True
            for j in range(1, max_refl+1):
                if rows[i-j] != rows[i+1+j]:
                    refl = False
                    break
            if refl: return i+1
    return None

def get_pattern_result(pattern: list[str], find_refl=find_refl1) -> int:

    res_refl = find_refl(pattern)
    if res_refl is not None:
        return res_refl * 100

    columns = ["".join([line[j] for line in pattern]) for j in range(0, len(pattern[0]))]
    res_refl = find_refl(columns)
    if res_refl is not None:
        return res_refl

    raise Exception("No reflection found!")

#%%

# part 1

patterns = read_lines(get_lines(test=False, testnb=1))
result = 0
for pattern in patterns:
    result += get_pattern_result(pattern)

print(result)

#%%

def cmp_rows(row1: str, row2: str) -> int:
    diff = 0
    for c1, c2 in zip(row1, row2):
        if c1 != c2:
            diff += 1
            if diff > 1:
                break
    return diff

def find_refl2(rows: list[str]) -> Optional[int]:
    for i, row in enumerate(rows[:-1]):
        diffs = cmp_rows(rows[i], rows[i+1])
        if diffs <= 1:
            max_refl = min(i, len(rows)-1 - (i+1))
            for j in range(1, max_refl+1):
                diffs += cmp_rows(rows[i-j], rows[i+1+j])
                if diffs > 1:
                    break
            if diffs == 1: return i+1
    return None

#%%

# part 2

patterns = read_lines(get_lines(test=False, testnb=1))
result = 0
for pattern in patterns:
    result += get_pattern_result(pattern, find_refl=find_refl2)

print(result)