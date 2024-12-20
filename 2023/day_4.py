#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 13:01:47 2024

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
        string = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
        lines = string.splitlines()
    
    else:
        # getting lines from input file
        with open('day_4.input', 'r') as file:
            lines = [l.strip() for l in file.readlines()]
        
    return lines


#%%

pattern_line = "Card\s+(\d+):\s+([\s\d]*\d)\s+\|\s+([\s\d]*\d)"
prog_line = re.compile(pattern_line)

space_pattern = "\s+"
prog_space = re.compile(space_pattern)

#%%

## part 1

def part1(lines):
    """ solves part 1 """
    score = 0
    for line in lines:
        m = prog_line.match(line)
        winning_numbers = [int(nb) for nb in prog_space.split(m.group(2))]
        my_numbers = [int(nb) for nb in prog_space.split(m.group(3))]
        n = len([nb for nb in my_numbers if nb in winning_numbers])
        if n > 0: 
            score += 2 ** (n-1)
    return score
        
#%%

# run part 1
score = part1(get_lines(test=False))
print(score)

#%%

test = False
lines = get_lines(test)

## part 2    

def part2(lines):
    cards = {}
    for line in lines:
        log(f"line: {line}")
        m = prog_line.match(line)
        card_id = int(m.group(1))
        nb_copies = cards.get(card_id, 0) + 1
        cards[card_id] = nb_copies
        winning_numbers = [int(nb) for nb in prog_space.split(m.group(2))]
        my_numbers = [int(nb) for nb in prog_space.split(m.group(3))]
        n = len([nb for nb in my_numbers if nb in winning_numbers])
        log(f"nb winning nbs: {n}")
        log(list(range(card_id + 1, card_id + 1 + n)))
        for cid in range(card_id + 1, card_id + 1 + n):
            if cid <= len(lines):
                cards[cid] = cards.get(cid, 0) + nb_copies

    log(cards)
    return sum(cards.values())
        
#%%

print(part2(get_lines(test=False)))


#%%

## unit testing

class Test(unittest.TestCase):
    
    def setUp(self):
        global logs
        logs = False

    def tearDown(self):
        global logs
        logs = True

    def test_part_1_string(self):
        lines = get_lines(test=True)
        self.assertEqual(part1(lines), 13)

    def test_part_1_file(self):
        lines = get_lines(test=False)
        self.assertEqual(part1(lines), 19855)
        
    def test_part_2_string(self):
        lines = get_lines(test=True)
        self.assertEqual(part2(lines), 30)
    
    def test_part_2_file(self):
        lines = get_lines(test=False)
        self.assertEqual(part2(lines), 10378710)
        

unittest.main()
