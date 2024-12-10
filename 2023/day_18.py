#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
# %%
import logging
import re
from coord import *

logging.basicConfig(level=logging.DEBUG, format="{message}", style="{")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


##
# %%

def get_lines(test: bool = False, testnb: int = 1) -> [str]:
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

        else:
            raise ValueError("Wrong testnb!")
        lines: [str] = string.splitlines()

    else:
        # getting lines from input file
        with open('2023/day_18.input', 'r') as file:
            lines: [str] = file.readlines()

    return [l.strip() for l in lines]


logger.debug(get_lines(test=True, testnb=1))

#%%

prog = re.compile(r"([RLUD]) (\d+) \(\#(\w+)\)")

#m = prog.match("R 6 (#70c710)")
#logger.debug(m.groups())

dir_map = { "R": "E", "L": "W", "U": "N", "D": "S" }

class Node:
    def __init__(self, pos: Coord, parent=None):
        self.pos = pos
        self.parent = parent
        self.dir_in = delta_to_direction(self.pos - self.parent.pos) if parent else "_"

    def get_next1(self, direction1: str) -> 'Node':
        direction = dir_map.get(direction1, direction1)
        return Node(self.pos + direction_to_delta(direction), self)

    def __str__(self) -> str:
        return f"({self.dir_in}>{self.pos})"

def read_lines(lines: [str]) -> [tuple]:
    node = Node(Coord(0, 0))
    records = []
    for line in lines:
        m = prog.match(line)
        dir1, steps, rgb = m.groups()
        steps = int(steps)
        records.append((dir, steps, rgb))
        for _ in range(steps):
            node = node.get_next1(dir1)
    return records, node


#%%

records, node = read_lines(get_lines(test=False, testnb=1))

current = node
x_min, x_max, y_min, y_max = None, None, None, None
while current is not None:
    logger.debug(current.pos)
    if x_min is None or current.pos.x < x_min:
        x_min = current.pos.x
    if x_max is None or current.pos.x > x_max:
        x_max = current.pos.x
    if y_min is None or current.pos.y < y_min:
        y_min = current.pos.y
    if y_max is None or current.pos.y > y_max:
        y_max = current.pos.y
    current = current.parent

logger.debug(f"x: {x_min} - {x_max}, y: {y_min} - {y_max}")


#%%
matrix = [[' ' for _ in range(x_max - x_min + 1)] for _ in range(y_max - y_min + 1)]
current = node
while current is not None:
    matrix[current.pos.y - y_min][current.pos.x - x_min] = '#'
    current = current.parent

for row in matrix:
    logger.debug("".join(row))