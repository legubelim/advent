#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:15:09 2024

@author: glg
"""
import math

test_string = """Time:      7  15   30
Distance:  9  40  200"""

test1_inputs = [{'time': 7, 'distance': 9 },
              {'time': 15, 'distance': 40 },
              {'time': 30, 'distance': 200 }
              ]

puzzle_string="""Time:        35     93     73     66
Distance:   212   2060   1201   1044"""

part1_inputs = [{'time': 35, 'distance': 212 },
              {'time': 93, 'distance': 2060 },
              {'time': 73, 'distance': 1201 },
              {'time': 66, 'distance': 1044 }
              ]

test1_inputs = [{'time': 71530, 'distance': 940200 }
              ]

part2_inputs = [{'time': 35937366, 'distance': 212206012011044 }
              ]

inputs = part2_inputs

result = 1
for inp in inputs:
    print(inp)
    a = -1
    b = inp['time']
    c = -inp['distance']
    delta = b**2 - 4*a*c
    n1 = (-b + math.sqrt(delta)) / (2*a)
    n2 = (-b - math.sqrt(delta)) / (2*a)
    print(f"n1: {n1}, n2: {n2}")
    nb_solutions = math.floor(n2) - math.ceil(n1) + 1
    nb_solutions -= int(math.ceil(n2) == n2) + int(math.floor(n1) == n1)
    print(f"nb solutions: {nb_solutions}")
    result *= nb_solutions
    
print(result)
    

