#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
from collections import namedtuple
from collections.abc import Iterable
from typing import Optional
import re

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

# part 1

def hash_line(options: [str]) -> int:
    res = 0
    for s in options:
        res += hash_option(s)
    return res

print(hash_line(read_line(get_lines(test=True, testnb=1))))

print(hash_line(read_line(get_lines(test=False, testnb=1))))

#%%

# part 2

class Lens:
    def __init__(self, label, focal):
        self.label = label
        self.focal = focal

    def __str__(self):
        return f"Lens(label: {self.label}, focal: {self.focal})"

    def __repr__(self):
        return f"{self.label} {self.focal}"


prog = re.compile(r"([^\-=]+)([\-=])(\d)*")

#%%

logger.setLevel(logging.INFO)
options = read_line(get_lines(test=False, testnb=1))

boxes = {}

for option in options:
    m = prog.match(option)
    #logger.debug(m.groups())
    label, operation, focal = m.groups()
    if focal is not None:
        focal = int(focal)
    boxnb = hash_option(label)
    box = boxes.setdefault(boxnb, [])

    logger.debug(f"label: {label}, operation: {operation}, focal: {focal}, boxnb: {boxnb}")
    logger.debug(f"box before: {box}")

    if operation == '-':
        box = [lens for lens in box if lens.label != label]
        boxes[boxnb] = box
    elif operation == '=':
        present = False
        for lens in box:
            if lens.label == label:
                present = True
                lens.focal = focal
        if not present:
            box.append(Lens(label, focal))
    logger.debug(f"box after: {box}")

logger.info(boxes)

#%%

result = 0
for box_id, box in boxes.items():
    box_result = 0
    for lens_id, lens in enumerate(box):
        box_result += (box_id + 1) * (lens_id + 1) * lens.focal
        logger.debug(f"{lens.label}: {box_id + 1} (box {box_id}) * {lens_id + 1} ({lens_id + 1}th slot) * {lens.focal} (focal length) = {(box_id + 1) * (lens_id + 1) * lens.focal}")
    result += box_result

print(result)

