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

#%%

# Part 1


class Node:
    def __init__(self, pos: Coord, parent=None):
        self.pos = pos
        self.parent = parent
        self.dir_in = delta_to_direction(self.pos - self.parent.pos) if parent else "_"

    def get_next1(self, direction1: str) -> 'Node':
        direction = dir_map.get(direction1, direction1)
        return Node(self.pos + direction_to_delta(direction), self)

    def get_right_cell(self) -> Coord:
        if self.dir_in == "N": return self.pos + direction_to_delta('E')
        if self.dir_in == "S": return self.pos + direction_to_delta('W')
        if self.dir_in == "E": return self.pos + direction_to_delta('S')
        if self.dir_in == "W": return self.pos + direction_to_delta('N')
        return None

    def __str__(self) -> str:
        return f"({self.dir_in}>{self.pos})"

def read_lines(lines: [str]) -> [tuple]:
    node = Node(Coord(0, 0))
    records = []
    for line in lines:
        m = prog.match(line)
        dir1, steps, rgb = m.groups()
        steps = int(steps)
        records.append((dir1, steps, rgb))
        for _ in range(steps):
            node = node.get_next1(dir1)
    return records, node


#%%

records, node = read_lines(get_lines(test=False, testnb=1))

positions = set()
current = node
x_min, x_max, y_min, y_max = None, None, None, None
while current is not None:
    positions.add(current.pos)
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

# %%

cells = set()
current = node
while current is not None:
    cell = current.get_right_cell()
    if (cell is not None) and (cell not in positions):
        cells.add(cell)
    current = current.parent

to_expand = list(cells)
while to_expand:
    cell = to_expand.pop(0)
    for pos in cell.get_neighbors():
        if pos not in positions:
            if pos not in cells:
                to_expand.append(pos)
            cells.add(pos)

for cell in cells:
    matrix[cell.y - y_min][cell.x - x_min] = '.'

for row in matrix:
    logger.debug("".join(row))

print(f" nb of inside cells: {len(cells) + len(positions)}")

#%% Part 2

class Segment:
    def __init__(self, dir: str, length: int, parent=None):
        self.parent = parent
        self.child = None
        if parent is None:
            self.start = Coord(0,0)
        else:
            self.start = parent.end
            parent.child = self
        self.dir = dir
        self.length = length
        self.end = self.start + direction_to_delta(dir) * length

    def __str__(self) -> str:
        return f"[{self.start} - {self.end}]"

    def __repr__(self) -> str:
        return self.__str__()

    def is_in(self, pos: Coord) -> bool:
        return (((self.start.x <= pos.x <= self.end.x) or (self.start.x >= pos.x >= self.end.x))
                and ((self.start.y <= pos.y <= self.end.y) or (self.start.y >= pos.y >= self.end.y)))
    def is_horizontal(self) -> bool:
        return self.dir in ["E", "W"]

    def is_crossing_row(self, y: int) -> bool:
        return (self.start.y <= y <= self.end.y) or (self.end.y <= y <= self.start.y)

    def is_end_wall(self) -> bool:
        return self.child.dir != self.parent.dir

dir_map2 = { "0": "E", "2": "W", "3": "N", "1": "S" }
def read_lines2(lines: [str], aspart1=False) -> [tuple]:
    segment = None
    segments = []
    records = []
    for line in lines:
        m = prog.match(line)
        dir1, steps, rgb = m.groups()
        if aspart1:
            dir2 = dir_map.get(dir1, dir1)
            length = int(steps)
        else:
            length = int(rgb[:5], 16)
            dir2 = dir_map2[rgb[5]]
        records.append((line, dir2, length))
        segment = Segment(dir2, length, segment)
        segments.append(segment)
    segments[0].parent = segments[-1]
    segments[-1].child = segments[0]
    return records, segments

#%%

def get_dimensions(segments: [Segment]) -> tuple:
    x_min, x_max, y_min, y_max = None, None, None, None
    for segment in segments:
        if x_min is None or segment.start.x < x_min:
            x_min = segment.start.x
        if x_min is None or segment.end.x < x_min:
            x_min = segment.end.x
        if x_max is None or segment.start.x > x_max:
            x_max = segment.start.x
        if x_max is None or segment.end.x > x_max:
            x_max = segment.end.x
        if y_min is None or segment.start.y < y_min:
            y_min = segment.start.y
        if y_min is None or segment.end.y < y_min:
            y_min = segment.end.y
        if y_max is None or segment.start.y > y_max:
            y_max = segment.start.y
        if y_max is None or segment.end.y > y_max:
            y_max = segment.end.y
    return x_min, x_max, y_min, y_max

def get_y_ends(segments: [Segment], y_min: int, y_max:int) -> [int]:
    """ returns a list of y coordinates where a segment starts or ends
        and also just before a segment starts or ends
    """
    y_ends = set()
    for segment in segments:
        y_ends.add(segment.start.y)
        if segment.start.y > y_min:
            y_ends.add(segment.start.y - 1)
        y_ends.add(segment.end.y)
        if segment.end.y > y_min:
            y_ends.add(segment.end.y - 1)
    return sorted(list(set(y_ends)))

#%%
def row_filling(min_x: int, segments: [Segment]) -> [[(int, int)], int]:
    """Based on the segments crossing a row at y, returns a list of tuples marking the start and end of filled areas"""
    is_between_verticals = False
    to_fill = []
    previous_x = min_x
    for s in segments:
        if s.is_horizontal():
            left_x, right_x = min(s.start.x, s.end.x), max(s.start.x, s.end.x)
            to_fill.append((left_x, right_x))
            if is_between_verticals:
                to_fill.append((previous_x, left_x - 1))
            if not s.is_end_wall():
                is_between_verticals = not is_between_verticals
            previous_x = right_x + 1
        else:
            if is_between_verticals:
                to_fill.append((previous_x, s.start.x))
            is_between_verticals = not is_between_verticals
            previous_x = s.start.x
    filled = sum([end - start + 1 for start, end in to_fill])
    return to_fill, filled



def get_row_segments(segments: [Segment], y: int) -> [Segment]:
    """ returns a list of segments crossing the row at y, useful for filling the row """
    horizontals = []
    verticals = []
    for segment in segments:
        if segment.is_crossing_row(y):
            if segment.is_horizontal():
                horizontals.append(segment)
            else:
                verticals.append(segment)
    items = []
    for v in verticals:
        if not any([h.is_in(v.start) or h.is_in(v.end) for h in horizontals]):
            items.append(v)
    items += horizontals
    items.sort(key=lambda s: s.start.x)
    return items

#%%

# Test part 2 - only works for small examples
# we can use the file but need to read it as in part 1
# we fill it in the new way and we compare with part 1 strategy

records, segments = read_lines2(get_lines(test=False), aspart1=True)
for record in records:
    logger.debug(record)

x_min, x_max, y_min, y_max = get_dimensions(segments)
y_ends = get_y_ends(segments, y_min, y_max)

logger.debug(f"x: [{x_min} - {x_max}], y: [{y_min} - {y_max}]")

matrix2 = [[' ' for _ in range(x_max - x_min + 1)] for _ in range(y_max - y_min + 1)]

surface = 0
for y in range(y_min, y_max + 1):
    items = get_row_segments(segments, y)
    #logger.debug(f"y: {y}, items: {items}")
    to_fill, filled = row_filling(x_min, items)
    logger.debug(f"y: {y}, to_fill: {to_fill}, filled: {filled}")
    surface += filled
    for start, end in to_fill:
        matrix2[y - y_min][start - x_min] = 'S'
        matrix2[y - y_min][end - x_min] = 'E'
        for x in range(start + 1, end):
            matrix2[y - y_min][x - x_min] = '.'

print(f"surface: {surface}")


for row in matrix:
    logger.debug("".join(row))

for row in matrix2:
    logger.debug("".join(row))


# displaying both at the same time to spot differences
for row1, row2 in zip(matrix, matrix2):
    logger.debug("".join(row1))
    logger.debug("".join(row2))


#%%

# running part 2 that scales

records, segments = read_lines2(get_lines(test=False), aspart1=False)
for record in records:
    logger.debug(record)

x_min, x_max, y_min, y_max = get_dimensions(segments)
y_ends = get_y_ends(segments, y_min, y_max)

logger.debug(f"x: [{x_min} - {x_max}], y: [{y_min} - {y_max}]")

surface = 0
last_y = None
for y in y_ends:
    items = get_row_segments(segments, y)
    to_fill, filled = row_filling(x_min, items)
    logger.debug(f"y: {y} (last_y: {last_y}), to_fill: {to_fill}, filled: {filled} x {y - last_y if last_y is not None else 1} = {filled * ((y - last_y) if last_y is not None else 1)}")
    surface += filled * ((y - last_y) if last_y is not None else 1)
    last_y = y

print(f"surface: {surface}")


