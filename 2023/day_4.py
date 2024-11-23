#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 13:01:47 2024

@author: glg
"""

import re

#%%

test = False

def get_lines(test=False):
    if test:
        
        string = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
        lines = string.splitlines()
    
    else:
        with open('day_4.input', 'r') as file:
            lines = [l.strip() for l in file.readlines()]
        
    return lines

lines = get_lines(test)

#%%

pattern_line = "Card\s+(\d+):\s+([\s\d]*\d)\s+\|\s+([\s\d]*\d)"
prog_line = re.compile(pattern_line)

space_pattern = "\s+"
prog_space = re.compile(space_pattern)

#%%

## part 1

def part1(lines):
    score = 0
    for line in lines:
        #print(f"line: {line}")
        m = prog_line.match(line)
        card_id = int(m.group(1))
        #print(m.group(2))
        winning_numbers = [int(nb) for nb in prog_space.split(m.group(2))]
        #print(m.group(3))
        #print([nb for nb in prog_space.split(m.group(3))])
        my_numbers = [int(nb) for nb in prog_space.split(m.group(3))]
        #print(m.group(3))
        #print(my_numbers)
        n = len([nb for nb in my_numbers if nb in winning_numbers])
        #print(f"nb winning nbs: {n} score: {2 ** (n-1) if n>0 else 0} ")
        if n > 0: 
            score += 2 ** (n-1)
    return score
        
#%%

score = part1(get_lines(test=False))
print(score)

#%%

## part 2    


#%%

import unittest

class Test(unittest.TestCase):

    def test_part_1_string(self):
        lines = get_lines(test=True)
        self.assertEqual(part1(lines), 13)

    def test_part_1_file(self):
        lines = get_lines(test=False)
        self.assertEqual(part1(lines), 19855)

unittest.main()
