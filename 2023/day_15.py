#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
from collections.abc import Iterable
from typing import Optional

logging.basicConfig(level=logging.DEBUG, format="{message}", style="{")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

##
#%%

def get_lines(test:bool=False, testnb:int=1) -> str:
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

        else:
            raise ValueError("Wrong testnb!")
        line = string

    else:
        # getting lines from input file
        with open('2023/day_15.input', 'r') as file:
            lines:[str] = file.readlines()
            line = lines[0]

    return line.strip()

logger.debug(get_lines(test=True, testnb=1))

#%%

def read_line(line: str) -> [str]:
    return line.split(',')

logger.debug(read_line(get_lines(test=True, testnb=1)))

#%%

def hash_option(s: str) -> int:
    result = 0
    for c in s:
        result += ord(c)
        result = (17 * result) % 256
    return result


print(hash_option("HASH"))

#%%

def hash_line(options: [str]) -> int:
    res = 0
    for s in options:
        res += hash_option(s)
    return res

print(hash_line(read_line(get_lines(test=True, testnb=1))))

print(hash_line(read_line(get_lines(test=False, testnb=1))))

#%%



