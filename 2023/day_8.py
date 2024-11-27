#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import re
import logging
import math

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

##
#%%

def get_lines(test=False, testnb=1):
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
        elif testnb == 2:
            string = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
        elif testnb == 3:
            string = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

        lines = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_8.input', 'r') as file:
            lines = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

##
#%%

pattern = r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)"
prog = re.compile(pattern)

def read_lines(lines):
    directions = lines[0]
    map = {}
    for line in lines[2:]:
        m = prog.match(line)
        map[m.group(1)] = (m.group(2), m.group(3))
    return directions, map

logger.debug(read_lines(get_lines(test=True, testnb=1)))

##
#%%


def compute_step_part1(directions, map):

    step = 0

    node = 'AAA'
    while node != 'ZZZ':
        node = map[node][0 if directions[step % len(directions)] == 'L' else 1]
        step += 1
    return step

##
#%%

directions, map = read_lines(get_lines(test=False, testnb=2))
print(compute_step_part1(directions, map))

##
#%%
# part 2 -- failing attempt: would require years to compute

def compute_step_part2_failing(directions, map):
    processed = set()
    step = 0
    nodes = [k for k in map.keys() if k[2] == 'A']
    logger.info(f"nodes: {nodes}")
    while not all([n[2] == 'Z' for n in nodes]):
        processed.add(tuple(nodes))
        new_nodes = []
        direction = 0 if directions[step % len(directions)] == 'L' else 1
        for node in nodes:
            logger.debug(f"{node} --> {map[node]}")
            new_nodes.append(map[node][direction])
        nodes = new_nodes
        reached = sum([n[2] == 'Z' for n in nodes])
        if reached > 2:
            logger.info(f"nodes: {nodes}")
            logger.info(f"nb xxZ {reached}")
        step += 1
        if tuple(nodes) in processed:
            print(f"loop on {nodes}")
            break
    return step


##
#%%

# part 2 - compute the least common multiple of the steps for each starting node

def compute_step_part2(directions, map):
    nodes = {k:0 for k in map.keys() if k[2] == 'A'}

    for start_node in nodes.keys():
        logger.info(f"start_node: {start_node}")
        node = start_node
        step = 0
        while node[2] != 'Z':
            node = map[node][0 if directions[step % len(directions)] == 'L' else 1]
            step += 1
        nodes[start_node] = step
        logger.info(f"step: {step}")
    return math.lcm(*nodes.values())

directions, map = read_lines(get_lines(test=False, testnb=2))
print(compute_step_part2(directions, map))

