#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:14:50 2024

@author: legubelim
"""

import re
import unittest

#%%

logs = True

def log(s):
    if logs:
        print(s)
    

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

        lines = string.splitlines()
    
    else:
        # getting lines from input file
        with open('day_5.input', 'r') as file:
            lines = [l.strip() for l in file.readlines()]
        
    return lines

print(get_lines(test=True))