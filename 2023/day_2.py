#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:12:25 2024

@author: glg
"""

import re

test_string = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

colors = ['red', 'blue', 'green']
color_pattern = "|".join(colors)

#%% 


test_string = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
print(f"string: {test_string}")
#test_string = "Game 1: "
pattern = "Game\s\d:(\s(\d)\s(" + color_pattern + "),?)+"
#pattern = "Game\s\d:\s\d\s(blue|red|green)" #(red)|(blue)|(green)"
pattern_game = "Game\s(\d):(.*)"
print(f"pattern: {pattern_game}")

prog_game = re.compile(pattern_game)
m_game = prog_game.match(test_string)
print(m_game)
if m_game:
    print(m_game.groups())

print()
test_string = m_game.group(2)
print(f"string: {test_string}")
pattern_draw = ";"
print(f"pattern: {pattern_draw}")

prog_draw = re.compile(pattern_draw)

split_draw = prog_draw.split(test_string)
print(split_draw)

print()
test_string = split_draw[0]
print(f"string: {test_string}")
pattern_color = ","

print(f"pattern: {pattern_color}")

prog_color = re.compile(pattern_color)

split_color = prog_color.split(test_string)
print(split_color)

print()
pattern_color = "\s*(\d)\s+(" + color_pattern + ")"
print(f"pattern: {pattern_game}")

test_string = split_color[0]
prog_game = re.compile(pattern_color)
m_color = prog_game.match(test_string)
print(m_color)
if m_game:
    print(m_color.groups())


#%%

for line in test_string.splitlines():
    
    
#%%


with open('day_2.input', 'r') as file:
    for l in file:
        line = l.strip()
        print(f"{line} --> ")
        

         