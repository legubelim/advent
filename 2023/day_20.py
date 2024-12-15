#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import logging
import re
from collections import namedtuple
from tarfile import TruncatedHeaderError
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
        with open('2023/day_20.input', 'r') as file:
            lines: [str] = file.readlines()

    return [l.strip() for l in lines]


logger.debug(get_lines(test=True, testnb=1))


#%%

#Pulse = namedtuple('Pulse', ['from_module', 'high_pulse', 'to_module'])

class Pulse:

    def __init__(self, from_module: str, high_pulse: bool, to_module: str):
        self.from_module = from_module
        self.high_pulse = high_pulse
        self.to_module = to_module

    def __str__(self):
        return f"{self.from_module} -{'high' if self.high_pulse else 'low'}-> {self.to_module}"

    def __repr__(self):
        return self.__str__()




class Module:

    def __init__(self, name: str, mtype=None, destinations: [str]=None):
        self.name = name
        self.mtype = mtype if mtype is not None else name
        self.destinations = destinations if destinations is not None else []
        if mtype == '%':
            self.on = False
        elif mtype == '&':
            self.inputs = {}

    def add_input(self, from_name):
        if self.mtype == '&':
            self.inputs[from_name] = False

    def __str__(self):
        if self.mtype == '%' :
            return f"({self.mtype}{self.name} -> {self.destinations} is_on: {self.on})"
        elif self.mtype == '&' :
            return f"({self.mtype}{self.name} -> {self.destinations} inputs: {self.inputs})"
        else:
            return f"({self.name} -> {self.destinations})"

    def __repr__(self):
        return self.__str__()

    def run(self, high_pulse=False, from_name=None):
        if self.mtype == 'broadcaster':
            return [Pulse(self.name, high_pulse, dest) for dest in self.destinations]
        elif self.mtype == 'output':
            return []
        elif self.mtype == 'button':
            return [Pulse(self.name, False, 'broadcaster')]
        elif self.mtype == '%':
            if high_pulse:
                return []
            else:
                self.on = not self.on
                if self.on:
                    return [Pulse(self.name, True, dest) for dest in self.destinations]
                else:
                    return [Pulse(self.name, False, dest) for dest in self.destinations]
        elif self.mtype == '&':
            self.inputs[from_name] = high_pulse
            if all(self.inputs.values()):
                return [Pulse(self.name, False, dest) for dest in self.destinations]
            else:
                return [Pulse(self.name, True, dest) for dest in self.destinations]




#%%

prog_module = re.compile(r"(\S+) -> (.+)")
prog_dest_sep = re.compile(", *")

def read_lines(lines: [str]) -> [Module]:
    modules = {}
    for line in lines:
        logger.debug(f"line: {line}")
        m_line = prog_module.match(line)
        destinations = prog_dest_sep.split(m_line.group(2))
        name = m_line.group(1)
        if name[0] in ['%', '&']:
            mtype = name[0]
            name = name[1:]
        else:
            mtype = name
        modules[name] = Module(name, mtype, destinations)
    #modules['output'] = Module('output')
    modules['button'] = Module('button', destinations=['broadcaster'])
    for name, module in modules.items():
        for dest in module.destinations:
            if dest in modules:
                modules[dest].add_input(name)
    return modules


#%%

# part 1

def run_sequence(modules):
    seq_pulses = []
    pulses_to_run = modules['button'].run()

    while pulses_to_run:
        seq_pulses += pulses_to_run
        new_pulses = []
        for pulse in pulses_to_run:
            if pulse.to_module in modules:
                new_pulses += modules[pulse.to_module].run(pulse.high_pulse, pulse.from_module)
        pulses_to_run = new_pulses

    for pulse in seq_pulses:
        logger.debug(pulse)

    high_pulse_nb = sum(p.high_pulse for p in seq_pulses)
    low_pulse_nb = len(seq_pulses) - high_pulse_nb
    return high_pulse_nb, low_pulse_nb

#%%

logger.setLevel(logging.INFO)

modules = read_lines(get_lines(test=False, testnb=2))
for module in modules.values():
    logger.debug(module)

high_pulse_nb, low_pulse_nb = 0, 0
for seq in range(1000):
    logger.debug(f"\n## Sequence {seq} ##")
    h, l = run_sequence(modules)
    high_pulse_nb += h
    low_pulse_nb += l
    logger.debug(f"## HIGH: {high_pulse_nb} LOW: {low_pulse_nb} ##")

print(f"result: {high_pulse_nb} x {low_pulse_nb} = {high_pulse_nb * low_pulse_nb}")

#%%
# part 2

def run_sequence2(modules):
    seq_pulses = []
    pulses_to_run = modules['button'].run()

    while pulses_to_run:
        seq_pulses += pulses_to_run
        new_pulses = []
        for pulse in pulses_to_run:
            if pulse.to_module in modules:
                new_pulses += modules[pulse.to_module].run(pulse.high_pulse, pulse.from_module)
        pulses_to_run = new_pulses

    rx_pulses = [p for p in seq_pulses if p.to_module == 'rx']
    high_pulse_nb = sum(p.high_pulse for p in rx_pulses)
    low_pulse_nb = len(rx_pulses) - high_pulse_nb
    return high_pulse_nb, low_pulse_nb

#%%

logger.setLevel(logging.DEBUG)

modules = read_lines(get_lines(test=False, testnb=2))
for module in modules.values():
    logger.debug(module)

all_pulses = []

seq = 0
while True:
    seq += 1
    h, l = run_sequence2(modules)
    if seq % 100000 == 0:
        logger.debug(f"## Sequence {seq}  HIGH: {h} LOW: {l}")
    if h == 0 and l == 1:
        break

print(f"result: {seq}")

