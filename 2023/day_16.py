#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
from collections import deque
from collections.abc import Iterable
from typing import Optional
import heapq

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
            string = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

        else:
            raise ValueError("Wrong testnb!")
        lines:[str] = string.splitlines()

    else:
        # getting lines from input file
        with open('2023/day_16.input', 'r') as file:
            lines:[str] = file.readlines()

    return [l.strip() for l in lines]

for line in get_lines(test=True, testnb=1):
    logger.debug(line)

#%%

tile_directions = {
    '|': {'E': ['N', 'S'], 'W': ['N', 'S'], 'N': ['N'], 'S': ['S']},
    '-': {'S': ['E', 'W'], 'N': ['E', 'W'], 'E': ['E'], 'W': ['W']},
    '/': {'E': ['N'], 'W': ['S'], 'N': ['E'], 'S': ['W']},
    '\\': {'E': ['S'], 'W': ['N'], 'N': ['W'], 'S': ['E']},
    '.': {'N': ['N'], 'S': ['S'], 'W': ['W'], 'E': ['E']}
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

    def get_tile(self, lines: [str]) -> str:
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

#%%

class Beam:

    def __init__(self, pos:Coord=Coord(0, 0), dir_in:str='E'):
        self.pos = pos
        self.dir_in = dir_in

    def next(self, lines) -> ['Beam']:
        max_x, max_y = len(lines[0]) -1, len(lines) -1
        tile = self.pos.get_tile(lines)
        #logger.debug(f"{self.pos} -> {tile} dir: {self.dir_in}")
        beams_out = []
        #logger.debug(f"next directions: {tile_directions[tile][self.dir_in]}")
        for dir in  tile_directions[tile][self.dir_in]:

            delta = direction_to_delta(dir)
            pos = self.pos + delta
            if pos.check_dimensions(max_x, max_y):
                beams_out.append(Beam(pos, dir))
        return beams_out

    def __repr__(self) -> str:
        return f"Beam({self.pos}->{self.dir_in})"

    def __str__(self) -> str:
        return f"Beam({self.pos}->{self.dir_in})"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other: 'Beam') -> bool:
        return (self.pos == other.pos) and (self.dir_in == other.dir_in)

    def __ne__(self, other: 'Beam') -> bool:
        return not self.__eq__(other)


#%%

def print_energized(lines: [str], beam_set: set[Beam]):

    energized = lines.copy()
    for beam in beam_set:
        energized[beam.pos.y] = energized[beam.pos.y][:beam.pos.x] + '#' + energized[beam.pos.y][beam.pos.x+1:]

    for line in lines:
        print(" " + line)

    print("")

    for line in energized:
        print(" " + line)
def energize(initial_beam: Beam, lines: [str], show=False) -> int:

    beams = deque([initial_beam])
    beam_set = set()

    while beams:
        beam = beams.popleft()
        logger.debug(f"Beam in: {beam}")
        beam_set.add(beam)
        for beam_out in beam.next(lines):
            logger.debug(f"  Beam out: {beam_out}")
            if beam_out not in beam_set:
                logger.debug("    -> is a new beam")
                beams.append(beam_out)
            else:
                logger.debug("    -> is already known")

    logger.debug(beam_set)

    if show:
        print_energized(lines, beam_set)

    return len(set([b.pos for b in beam_set]))

#%%

# part 1

logger.setLevel(logging.INFO)
lines = get_lines(test=False, testnb=1)

initial_beam = Beam()
print(f"--> energized: {energize(initial_beam, lines, True)}")

#%%

# part 2

logger.setLevel(logging.INFO)
lines = get_lines(test=False, testnb=1)

max_energy = 0

for y in range(0, len(lines)):
    initial_beam = Beam(Coord(0, y), 'E')
    energy = energize(initial_beam, lines)
    if energy > max_energy:
        max_energy = energy
    initial_beam = Beam(Coord(len(lines[0]) -1, y), 'W')
    energy = energize(initial_beam, lines)
    if energy > max_energy:
        max_energy = energy

for x in range(0, len(lines[0])):
    initial_beam = Beam(Coord(x, 0), 'S')
    energy = energize(initial_beam, lines)
    if energy > max_energy:
        max_energy = energy
    initial_beam = Beam(Coord(x, len(lines) -1), 'N')
    energy = energize(initial_beam, lines)
    if energy > max_energy:
        max_energy = energy

print(f"--> max energized: {max_energy}")




