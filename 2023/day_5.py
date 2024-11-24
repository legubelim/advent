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
    #print(m.group(1))
    seeds = [int(s) for s in sep_prog.split(m.group(1))]
    
    #print(seeds)
    
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
        #print(f"line: {line}")
        if line == "": continue
        new_map = False
        for map_name in maps:
            if line.find(map_name) != -1:
                #print(map_name)
                current_map = maps[map_name]
                new_map = True
                break
        #print(new_map)
        if new_map: continue
        m = map_line_prog.match(line)
        map_line = MapLine(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        #print(map_line)
        current_map.append(map_line)
        
    return seeds, maps

#%%

seeds, maps = read_maps(get_lines(test=False))

print(seeds)
print(maps)

#%%

def apply_map_line(seed:int, map_line:MapLine) -> Optional[int]:
    if (seed >= map_line.source_range_start) and (seed <= map_line.source_range_start + map_line.range_length):
        #print(map_line)
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
        #print(f"apply {map_name} to {source}")
        source = apply_map(source, cmap)
        #print(f"   --> {source}")
    locations.append(source)
    
print(locations)
print(min(locations))
   
             
    
    