#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:14:50 2024

@author: legubelim
"""

from typing import Optional
import re
from collections import namedtuple


#%%

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
    

#%%


def get_lines(test=False):
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        string = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37"""

        lines = [l.strip() for l in string.splitlines()]
    
    else:
        # getting lines from input file
        with open('day_5.input', 'r') as file:
            lines = file.readlines()
        
    return [l.strip() for l in lines]

logger.debug(get_lines(test=True))


#%%

MapLine = namedtuple('MapLine', 'destination_range_start source_range_start range_length')

def read_maps(lines):
    
    seeds = []
    
    seeds_pattern = "seeds:\s*([\d\s]+\d)"
    seeds_prog = re.compile(seeds_pattern)
    
    sep_pattern = "\s+"
    sep_prog = re.compile(sep_pattern)
    
    map_line_pattern = "\s*(\d+)\s+(\d+)\s+(\d+)"
    map_line_prog = re.compile(map_line_pattern)
    
    
    
    
    m = seeds_prog.match(lines[0])
    
    seeds = [int(s) for s in sep_prog.split(m.group(1))]
    
    logger.debug(seeds)
    
    maps = {"seed-to-soil": [],
            "soil-to-fertilizer": [],
            "fertilizer-to-water": [],
            "water-to-light": [],
            "light-to-temperature": [],
            "temperature-to-humidity": [],
            "humidity-to-location": []
            }
    
    current_map = None
    
    for line in lines[1:]:
        logger.debug(f"line: {line}")
        if line == "": continue
        new_map = False
        for map_name in maps:
            if line.find(map_name) != -1:
                logger.debug(map_name)
                current_map = maps[map_name]
                new_map = True
                break
        logger.debug(new_map)
        if new_map: continue
        m = map_line_prog.match(line)
        map_line = MapLine(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        logger.debug(map_line)
        current_map.append(map_line)
        
    return seeds, maps

#%%

seeds, maps = read_maps(get_lines(test=False))

logger.info(seeds)
logger.info(maps)

#%%

def apply_map_line(seed:int, map_line:MapLine) -> Optional[int]:
    if (seed >= map_line.source_range_start) and (seed <= map_line.source_range_start + map_line.range_length):
        #logger.debug(map_line)
        return map_line.destination_range_start + seed - map_line.source_range_start
    else:
        return None
    
def apply_map(seed, cmap) -> int:
    for map_line in cmap:
        destination = apply_map_line(seed, map_line)
        if destination is not None: 
            return destination
    return seed

#%%

## part 1
    
locations = []
for seed in seeds:
    source = seed
    for map_name, cmap in maps.items():
        logger.debug(f"apply {map_name} to {source}")
        source = apply_map(source, cmap)
        logger.debug(f"   --> {source}")
    locations.append(source)
    
logger.info(locations)
print(min(locations))
   
#%%

## part 2 -- Failed attempt because of performances

seeds, maps = read_maps(get_lines(test=True))

locations = []
for i in range(0, len(seeds), 2):
    seed_range_start, seed_range_end = seeds[i], seeds[i] + seeds[i+1] - 1
    logger.debug((seed_range_start, seed_range_end))
    for seed in range(seed_range_start, seed_range_end+1):
        source = seed
        for map_name, cmap in maps.items():
            logger.debug(f"apply {map_name} to {source}")
            source = apply_map(source, cmap)
            logger.debug(f"   --> {source}")
        locations.append(source)
        
logger.info(locations)
print(min(locations))
             
#%%

class interval:
    def __init__(self, start, end=None, length=1):
        self.start = start
        if end is not None:
            self.end = end
            self.length = end - start + 1
        else:
            self.length = length
            self.end = start + length - 1
        
    def __add__(self, o):
        if (self.end < o.start - 1) or (o.end < self.start - 1):
            return [self, o]
        else:
            return [interval(min(self.start, o.start), end=max(self.end, o.end))]
    
    def __sub__(self, o):
        if (self.end < o.start - 1) or (o.end < self.start-1):
            return [self]
        elif (o.start <= self.start) and (o.end >= self.start):
            return []
        elif o.start <= self.start:
            return [interval(o.end + 1, end=self.end)]
        elif o.end >= self.end:
            return [interval(self.start, end=o.start-1)]
        else:
            return [interval(self.start, end=o.start-1), interval(o.end + 1, end=self.end)]
        
    def __and__(self, o):
        if (self.end < o.start - 1) or (o.end < self.start-1):
            return None
        else:
            return interval(max(self.start, o.start), end=min(self.end, o.end))
        
    def translate(self, shift):
        return interval(self.start + shift, end=self.end + shift)
        
    def __str__(self):
        return f"[{self.start}..{self.end}]"
    
def invs2str(array):
    return "[" + ", ".join([f"{i}" for i in array]) +  "]"
    
   
a = interval(3, end=9)
b = interval(10, end=15)
c = interval(17, end=23)
d = interval(5, end=7)
e = interval(12, length=1)
f = interval(6, end=13)
logger.debug(f"a: {a}")
logger.debug(f"b: {b}")
logger.debug(f"c: {c}")
logger.debug(f"d: {d}")
logger.debug(f"e: {e}")
logger.debug(f"f: {f}")

logger.debug(f"a+b: {invs2str(a+b)}")
logger.debug(f"b+c: {invs2str(b+c)}")
logger.debug(f"a-d: {invs2str(a-d)}")

logger.debug(f"a-f: {invs2str(a-f)}")
logger.debug(f"a&f: {a&f}")

    
#%%

#seed_ranges = [(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2)]
#logger.debug(seed_ranges)
seeds, maps = read_maps(get_lines(test=False))

seed_ranges = [interval(seeds[i], length=seeds[i+1]) for i in range(0, len(seeds), 2)]
logger.info(invs2str(seed_ranges))



#%%

source_ranges = seed_ranges
for map_name, cmap in maps.items():
    dest_ranges = []
    for map_line in cmap:
        map_source_range = interval(map_line.source_range_start, length=map_line.range_length)        
        map_dest_range   = interval(map_line.destination_range_start, length=map_line.range_length)
        shift = map_line.destination_range_start - map_line.source_range_start
        
        new_source_ranges = []
        for source_range in source_ranges:
            mapped_source_range = source_range & map_source_range
            if mapped_source_range is not None:
                dest_ranges.append(mapped_source_range.translate(shift))
                new_source_ranges += source_range-mapped_source_range
            else:
                new_source_ranges.append(source_range)
        source_ranges = new_source_ranges
    source_ranges += dest_ranges
    
logger.info(invs2str(source_ranges))

print(min([i.start for i in source_ranges]))
            
    
   
