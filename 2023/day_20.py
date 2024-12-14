#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
import re
from typing import Optional

logging.basicConfig(level=logging.DEBUG, format="{message}", style="{")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


##
#%%

def get_lines(test: bool = False, testnb: int = 1) -> [str]:
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

        elif testnb == 2:
            string = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

        else:
            raise ValueError("Wrong testnb!")
        lines: [str] = string.splitlines()

    else:
        # getting lines from input file
        with open('2023/day_19.input', 'r') as file:
            lines: [str] = file.readlines()

    return [l.strip() for l in lines]


logger.debug(get_lines(test=True, testnb=1))


