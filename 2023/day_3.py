#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:38:54 2024

@author: glg
"""

import re

#%%

test = False

if test:
    
    string = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    lines = string.splitlines()

else:
    with open('day_3.input', 'r') as file:
        lines = [l.strip() for l in file.readlines()]
        
#%%

pattern = "\d+"
prog = re.compile(pattern)

#%%

def get_neighbors(lines, line_nb, span):
    line_size = len(lines[0])
    neighbors = []
    col_min = span[0] - 1
    col_max = span[1] + 1
    if line_nb > 0:
        neighbors += [(line_nb-1, col) for col in range(max(col_min, 0), min(col_max, line_size))]
    if col_min >= 0:
        neighbors.append((line_nb, col_min))
    if col_max <= line_size:
        neighbors.append((line_nb, col_max-1))
    if line_nb < len(lines)-1:
        neighbors += [(line_nb+1, col) for col in range(max(col_min, 0), min(col_max, line_size))]
    return neighbors
    
    

#%%

## part 1

result = 0
for line_nb, line in enumerate(lines):
    print(f"line_nb: {line_nb}  line: {line}")
    for m in prog.finditer(line):
        print(m)
        for row, col in get_neighbors(lines, line_nb, m.span()):
            #print(f"row: {row}, col: {col}")
            c = lines[row][col]
            if (c != '.') and (not c.isnumeric()):
                result += int(m.group(0))
                break
            
print(result)

#%%

## part 2

pattern_star = "\*"
prog_star = re.compile(pattern_star)

stars = {}
for line_nb, line in enumerate(lines):
    print(f"line_nb: {line_nb}  line: {line}")
    for m in prog_star.finditer(line):
        stars[(line_nb, m.start())] = []
        
print(stars)

for line_nb, line in enumerate(lines):
    print(f"line_nb: {line_nb}  line: {line}")
    for m in prog.finditer(line):
        print(m)
        for row, col in get_neighbors(lines, line_nb, m.span()):
            if (row, col) in stars:
                stars[(row, col)].append(int(m.group(0)))

print(stars)

result = 0
for _, value in stars.items():
    if len(value) == 2:
        result += value[0] * value[1]
        
print(result)
            



                
        
