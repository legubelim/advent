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

def get_lines(test:bool=False, testnb:int=1) -> [str]:
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        if testnb == 1:
            string = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
        elif testnb == 2:
            string = "????#???????#????? 1,8,1,1,1"

        else:
            raise ValueError("Wrong testnb!")
        lines:[str] = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_12.input', 'r') as file:
            lines:[str] = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True, testnb=1))

#%%

def read_lines(lines: [str], unfold=1) -> Iterable[dict]:
    records = []
    for line in lines:
        record = {}
        row_str, sizes_str = line.split(" ")
        row_str = "?".join([row_str for _ in range(unfold)])
        sizes_str = ",".join([sizes_str for _ in range(unfold)])
        row = [c for c in row_str]
        row.append('E')
        row = "".join(row)
        sizes = [int(s) for s in sizes_str.split(',')]
        record['row'], record['sizes'] = row, sizes
        records.append(record)
    return records


records = read_lines(get_lines(test=True))
for r in records:
    logger.debug(r)


#%%



#%%

def get_row_combis(row: str, sizes: Iterable[int], cache:Optional[dict]=None) -> int:
    logger.info(f"row: {row}, sizes {sizes}")
    global complexity
    complexity += 1
    if complexity % 1000000 == 0:
        logger.info(f"reaching complexity {complexity}")
    if len(sizes) == 0:
        if '#' not in row:
            logger.debug(f"finished: return 1")
            combis = 1
        else:
            logger.debug(f"finished but some # un-accounted for: return 0")
            combis = 0
    elif (len(row) < sum(sizes)) or (('?' not in row) and ('#' not in row)):
        logger.debug(f"impossible to fit {sizes} # (1): return 0")
        combis = 0
    elif sum(sizes) > sum([int(c == '?' or c == '#') for c in row]):
        logger.debug(f"impossible to fit {sizes} # (2): return 0")
        combis = 0
    elif sum(sizes) < sum([int(c == '#') for c in row]):
        logger.debug(f"impossible to include all # : return 0")
        combis = 0
    else:
        size = sizes[0]
        logger.debug(f"size: {size}")
        next_start = next(i for i, c in enumerate(row) if (c == '?') or (c == '#'))
        logger.debug(f"next_q: {next_start}")
        new_row = row[next_start:]
        logger.debug(f"new_row: {new_row}")
        if cache is not None:
            key = new_row + "_" + ",".join([str(s) for s in sizes])
            if key in cache:
                logger.debug(f"found in cache: returning {cache[key]}")
                return cache[key]
        max_size = next(i for i, c in enumerate(new_row) if (c != '?') and (c != '#'))
        logger.debug(f"max size: {max_size}")
        if size > max_size:
            logger.debug(f"impossible to fit {size} # (3): combis1 = 0")
            combis1 = 0
        elif new_row[size] == '#':
            logger.debug(f"series of # next to each other: combis1 = 0")
            combis1 = 0
        else:
            if new_row[size] == '?':
                logger.debug(f"skipping a ? to avoid contiguous series of #")
                combis1 = get_row_combis(new_row[size+1:], sizes[1:], cache)
            else:
                combis1 = get_row_combis(new_row[size:], sizes[1:], cache)
        if new_row[0] == '#':
            combis2 = 0
        else:
            combis2 = get_row_combis(new_row[1:], sizes, cache)
        combis  = combis1 + combis2
        if cache is not None:
            cache[key] = combis
    return combis

#%%

def compute_result(records):
    global complexity
    result = 0
    for record in records:
        logger.warning(f"record: {record}")
        complexity = 0
        combis = get_row_combis(record['row'], record['sizes'], cache={})
        logger.warning(f"   --> combis: {combis} complexity: {complexity}")
        result += combis
    logger.warning(f"TOTAL RESULT: {result}")
    return result

#%%
# part 1
logger.setLevel(logging.WARNING)
records = read_lines(get_lines(test=False), unfold=1)
result = compute_result(records)
print(result)

#%%
# part 2
logger.setLevel(logging.WARNING)
records = read_lines(get_lines(test=False), unfold=5)
result = compute_result(records)
print(result)


#%%

## unit testing

class Test:

    def assertEqual(self, res, ref):
        if res != ref:
            raise Exception(f"Test failed: result={res}, ref={ref}")
        else:
            print(f"Test passed: result={res}, ref={ref}")

    def setUp(self):
        logger.setLevel(logging.ERROR)

    def test_test_folded(self):
        records = read_lines(get_lines(test=True))
        result = compute_result(records)
        self.assertEqual(result, 21)

    def test_file_folded(self):
        records = read_lines(get_lines(test=False))
        result = compute_result(records)
        self.assertEqual(result, 7753)

    def test_test_unfolded(self):
        records = read_lines(get_lines(test=True), unfold=5)
        result = compute_result(records)
        self.assertEqual(result, 525152)

    def test_file_unfolded(self):
        records = read_lines(get_lines(test=False), unfold=5)
        result = compute_result(records)
        self.assertEqual(result, 280382734828319)

    def run(self):
        self.setUp()
        self.test_test_folded()
        self.test_file_folded()
        self.test_test_unfolded()
        self.test_file_unfolded()


test = Test()
test.run()

