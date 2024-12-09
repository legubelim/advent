#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
# %%
import logging
import heapq

import os, sys
#sys.path.append(os.path.dirname(__file__))
#print(sys.path)
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
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

        else:
            raise ValueError("Wrong testnb!")
        lines: [str] = string.splitlines()

    else:
        # getting lines from input file
        with open('2023/day_17.input', 'r') as file:
            lines: [str] = file.readlines()

    return [l.strip() for l in lines]


logger.debug(get_lines(test=True, testnb=1))




# %%
class Node:
    def __init__(self, pos: Coord, parent=None):
        self.pos = pos
        self.parent = parent
        self.len = parent.len + int(pos.get_value()) if self.parent else 0
        self.dir_in = delta_to_direction(self.pos - self.parent.pos) if parent else "_"
        if parent:
            self.dir_in_in_a_row = 1
            if parent.dir_in == self.dir_in:
                self.dir_in_in_a_row += self.parent.dir_in_in_a_row
        else:
            self.dir_in_in_a_row = 0

    # TODO hash and eq
    # TODO neighbors (in order of path length)
    # TODO meet node from opposite corner

    def get_neighbors(self) -> ['Node']:
        neighbors = []
        for neighbor in self.pos.get_neighbors():
            if (((self.parent is None) or (neighbor != self.parent.pos))
                and ((self.dir_in_in_a_row < 3) or (neighbor != self.pos.get_next(self.dir_in)))):
                neighbors.append(Node(neighbor, self))
        return neighbors

    def get_neighbors2(self) -> ['Node']:
        neighbors = []
        if (self.parent is not None) and (self.dir_in_in_a_row < 4):
            next_pos = self.pos.get_next(self.dir_in)
            if next_pos is not None:
                neighbors.append(Node(next_pos, self))
        else:
            for neighbor in self.pos.get_neighbors():
                if (
                        ((self.parent is None) or (neighbor != self.parent.pos))
                    and ((self.dir_in_in_a_row < 10) or (neighbor != self.pos.get_next(self.dir_in)))
                ):
                    neighbors.append(Node(neighbor, self))
        return neighbors

    def get_min_len_to_target(self, target: Coord) -> int:
        return self.len + self.pos.get_manhattan_dist(target)

    def key(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"({self.dir_in_in_a_row}{self.dir_in}>{self.pos})"

    def __repr__(self) -> str:
        return f"Node({self.dir_in_in_a_row}{self.dir_in}>{self.pos})"

    def __lt__(self, other: 'Node') -> bool:
        return (self.len < other.len
                or ((self.len == other.len) and (self.dir_in_in_a_row < other.dir_in_in_a_row)))

    def __gt__(self, other):
        return other < self
    def __eq__(self, other: 'Node') -> bool:
        return (self.pos == other.pos) and (self.dir_in == other.dir_in) and (self.dir_in_in_a_row == other.dir_in_in_a_row)

#%%

def print_visited(visited: dict[str, Node], lines: [str], current: Node=None):
    node_str = lines.copy()
    for node in visited.values():
        node_str[node.pos.y] = node_str[node.pos.y][:node.pos.x] + '#' + node_str[node.pos.y][node.pos.x+1:]
    if current:
        node_str[current.pos.y] = node_str[current.pos.y][:current.pos.x] + '*' + node_str[current.pos.y][current.pos.x + 1:]

    for line in node_str:
        print(line)
    print()


#%%

# part 1

lines = get_lines(test=False)
Coord.set_matrix(lines)

origin = Node(Coord(0,0))
destination = Node(Coord(len(lines[0])-1, len(lines)-1))

visited = {origin.key(): origin}
queue = [(origin.get_min_len_to_target(destination.pos), origin)]

steps = 0

while queue:
    _, current = heapq.heappop(queue)
    #print_visited(visited, lines, current)

    if current.pos == destination.pos:
        break
    for neighbor in current.get_neighbors():
        key = neighbor.key()
        if (key not in visited) or (neighbor.len < visited[key].len):
            visited[neighbor.key()] = neighbor
            #print(f"pushing {neighbor} with distance {neighbor.get_min_len_to_target(destination.pos)}")
            heapq.heappush(queue, (neighbor.get_min_len_to_target(destination.pos), neighbor))
    steps += 1


print(f"path length: {current.len}")

#%%

path_str = lines.copy()
path = current
while path is not None:
    print(path)
    path_str[path.pos.y] = path_str[path.pos.y][:path.pos.x] + '#' + path_str[path.pos.y][path.pos.x+1:]
    path = path.parent

for line in path_str:
    print(line)

#%%

# part 2

lines = get_lines(test=False)
Coord.set_matrix(lines)

origin = Node(Coord(0,0))
destination = Node(Coord(len(lines[0])-1, len(lines)-1))

visited = {origin.key(): origin}
queue = [(origin.get_min_len_to_target(destination.pos), origin)]

steps = 0

while queue:
    _, current = heapq.heappop(queue)
    #print_visited(visited, lines, current)

    if (current.pos == destination.pos) and (current.dir_in_in_a_row >= 4):
        break
    for neighbor in current.get_neighbors2():
        key = neighbor.key()
        if (key not in visited) or (neighbor.len < visited[key].len):
            visited[neighbor.key()] = neighbor
            #print(f"pushing {neighbor} with distance {neighbor.get_min_len_to_target(destination.pos)}")
            heapq.heappush(queue, (neighbor.get_min_len_to_target(destination.pos), neighbor))
    steps += 1


print(f"path length: {current.len}")

