#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 22:41:33 2024

@author: glg
"""
#%%

numbers = {"one": 1, 
           "two": 2, 
           "three": 3,
           "four": 4,
           "five": 5,
           "six": 6,
           "seven": 7,
           "eight": 8,
           "nine":9
           }

#%%

def get_digits_from_line(line):
    digits=""
    for c in line:
        if c.isnumeric():
            digits += c
            break
    for c in reversed(line):
        if c.isnumeric():
            digits += c
            break
    return int(digits)

#%%

def get_digits_from_line2(line):
    digits=[]
    
    for idx, c in enumerate(line):
        if c.isnumeric():
            digits.append((idx, int(c)))

    for nb in numbers.keys():
        idx = line.find(nb)
        # attention: the same nb can be found several times!
        while idx != -1:
            digits.append((idx, numbers[nb]))
            idx = line.find(nb, idx + 1)
            
            
    sorted_digits = sorted(digits)
    
    return int(sorted_digits[0][1] * 10 + sorted_digits[-1][1])

#%%

test_string = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

result = 0
for line in test_string.splitlines():
    digits = get_digits_from_line2(line)
    result += digits
    print(f"{line} --> {digits}")
    
print(result)

#%%

with open('day_1.input', 'r') as file:
    result = 0
    for l in file:
        line = l.strip()
        #digits = get_digits_from_line1(line)
        digits = get_digits_from_line2(line)
        result += digits
        print(f"{line} --> {digits}")
        
    print(result)

         