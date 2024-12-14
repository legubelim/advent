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
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

        else:
            raise ValueError("Wrong testnb!")
        lines: [str] = string.splitlines()

    else:
        # getting lines from input file
        with open('2023/day_19.input', 'r') as file:
            lines: [str] = file.readlines()

    return [l.strip() for l in lines]


logger.debug(get_lines(test=True, testnb=1))





#%%

workflow_prog = re.compile(r"(\w+){(.*)}")
rules_prog = re.compile(r"(\w+)([<>=])(\d+):(\w+)")
part_prog = re.compile(r"{(.*?)}")
rating_prog = re.compile(r"(\w+)=(\d+)")

class Rule:
    def __init__(self, next_workflow_name, rating=None, op=None, value=None):
        self.rating = rating
        self.op = op
        self.value = value
        self.next_workflow_name = next_workflow_name

    def apply_to_part(self, part):
        logger.debug(f"rule: {self}, part: {part}")
        if self.op is None:
            return self.next_workflow_name
        elif self.op == "<" and part[self.rating] < self.value:
            return self.next_workflow_name
        elif self.op == ">" and part[self.rating] > self.value:
            return self.next_workflow_name
        elif self.op == "=" and part[self.rating] == self.value:
            return self.next_workflow_name
        return None

    def __str__(self):
        if self.op is None:
            return f"{self.next_workflow_name}"
        else:
            return f"{self.rating}{self.op}{self.value}:{self.next_workflow_name}"

    def __repr__(self):
        return self.__str__()

def read_lines(lines):
    workflows = {}
    parts = []
    workflow_phase = True
    for line in lines:
        logger.debug(f"line: {line}")
        if line == "":
            workflow_phase = False
            continue
        if workflow_phase:
            workflow_m = workflow_prog.match(line)
            name = workflow_m.group(1)
            rules = []
            for rule_str in workflow_m.group(2).split(","):
                rule_m = rules_prog.match(rule_str)
                if rule_m is None:
                    rules.append(Rule(rule_str))
                else:
                    rules.append(Rule(rule_m.group(4), rule_m.group(1), rule_m.group(2), int(rule_m.group(3))))
            workflows[name] = rules
            logger.debug(f"{name}: {rules}")
        else:
            part = {}
            part_m = part_prog.match(line)
            for part_str in part_m.group(1).split(","):
                part_m = rating_prog.match(part_str)
                part[part_m.group(1)] = int(part_m.group(2))
            parts.append(part)
            logger.debug(part)
    return workflows, parts




#%%

# part 1

def apply_workflow(workflow, part):
    for rule in workflow:
        next_workflow_name = rule.apply_to_part(part)
        if next_workflow_name is not None:
            return next_workflow_name
    raise ValueError("No rule applied")

def apply_workflows(workflows, part):
    workflow_name = "in"
    while workflow_name not in [None, 'A', 'R']:
        workflow = workflows[workflow_name]
        workflow_name = apply_workflow(workflow, part)
    if workflow_name == 'A':
        return True
    if workflow_name == 'R':
        return False
    raise ValueError("Wrong workflow")


workflows, parts = read_lines(get_lines(test=False, testnb=1))
result = 0
for part in parts:
    if apply_workflows(workflows, part):
        result += sum(part.values())

print(f"sum of ratings: {result}")

#%%

# part 2

class Combi:
    rating_keys = ['a', 'm', 's', 'x']

    def __init__(self,):
        self.ranges = {}
        for key in self.rating_keys:
            self.ranges[key] = {}
            self.ranges[key]['min'] = 1
            self.ranges[key]['max'] = 4000

    def nbcombis(self):
        n = 1
        for key in self.rating_keys:
            n *= self.ranges[key]['max'] - self.ranges[key]['min'] + 1
        return n

    def copy(self):
        cp = Combi()
        for key in self.rating_keys:
            cp.ranges[key]['min'] = self.ranges[key]['min']
            cp.ranges[key]['max'] = self.ranges[key]['max']
        return cp

    def __str__(self):
        return "(" + ",".join([f"{k}:[{r['min'], r['max']}]" for k, r in self.ranges.items()]) + ")"

    def __repr__(self):
        return self.__str__()

    def split(self, rating, value):
        if self.ranges[rating]['min'] < value <= self.ranges[rating]['max']:
            combi1 = self.copy()
            combi1.ranges[rating]['max'] = value - 1
            combi2 = self.copy()
            combi2.ranges[rating]['min'] = value
            #logger.debug(f"splitting {self} on {rating}:{value} --> {combi1} | {combi2}")
            return (combi1, combi2)
        else:
            raise ValueError(f"cannot split {self} on {rating}:{value}")

    def apply_rule(self, rule:Rule) -> [['Combi', bool, Optional[str]]]:
        if rule.op is None:
            if rule.next_workflow_name == 'R':
                return []
            else:
                return [(self, True, rule.next_workflow_name)]
        elif rule.op == "<":
            if self.ranges[rule.rating]['max'] < rule.value:
                return [(self, True, rule.next_workflow_name)]
            elif self.ranges[rule.rating]['min'] >= rule.value:
                return [(self, False, None)]
            else:
                combi1, combi2 = self.split(rule.rating, rule.value)
                return [(combi1, True, rule.next_workflow_name), (combi2, False, None)]
        elif rule.op == ">":
            if self.ranges[rule.rating]['max'] <= rule.value:
                return [(self, False, None)]
            elif self.ranges[rule.rating]['min'] > rule.value:
                return [(self, True, rule.next_workflow_name)]
            else:
                combi1, combi2 = self.split(rule.rating, rule.value + 1)
                return [(combi1, False, None), (combi2, True, rule.next_workflow_name)]
        else:
            raise ValueError(f"Unknown operator {rule.op}")

#%%

def apply_workflow(combi: Combi, workflow_name, workflows, accepted):
    if workflow_name == 'A':
        accepted.append(combi)
        return
    if workflow_name == 'R':
        return
    workflow = workflows[workflow_name]

    for rule in workflow:
        for item in combi.apply_rule(rule):
            if item[1]:
                apply_workflow(item[0], item[2], workflows, accepted)
            else:
                combi = item[0]

accepted = []
apply_workflow(Combi(), 'in', workflows, accepted)

result = 0
for a in accepted:
    result += a.nbcombis()

print(result)
