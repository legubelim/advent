#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

##
#%%

def get_lines(test=False, testnb=1):
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
        elif testnb == 2:
            string = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

        lines = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_8.input', 'r') as file:
            lines = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

##
#%

