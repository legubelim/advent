
##
#%%
import re
import logging
import math

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

##
#%%

def get_lines(test=False):
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        string = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

        lines = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_9.input', 'r') as file:
            lines = file.readlines()

    return [l.strip() for l in lines]

logger.debug(get_lines(test=True))

#%%

sep_pattern = r"\s+"
sep_prog = re.compile(sep_pattern)

def read_lines(lines):
    histories = []
    for line in lines:
        logger.debug(f"line: {line}")
        values = [int(v) for v in sep_prog.split(line)]

        pyramid = [values]
        diffs = values
        while not all([d==0 for d in diffs]):
            diffs = [diffs[i+1] - diffs[i] for i in range(0, len(diffs)-1)]
            pyramid.append(diffs)

        pyramid = list(reversed(pyramid))
        logger.debug(pyramid)
        for i in range(0, len(pyramid)-1):
            diffs = pyramid[i]
            pyramid[i+1].append(pyramid[i+1][-1] + diffs[-1])
            #pyramid[i+1].prepend(pyramid[i+1][-1] - diffs[0])
            pyramid[i+1] = [pyramid[i+1][0] - diffs[0]] + pyramid[i+1]
        next_value = pyramid[-1][-1]
        previous_value = pyramid[-1][0]
        history = {'values': values,
                   'pyramid': pyramid,
                   'next_value': next_value,
                   'previous_value': previous_value}
        histories.append(history)
        logger.debug(history)

    return histories

#%%

histories = read_lines(get_lines(test=False))
# part 1
print(sum([h['next_value'] for h in histories]))
# part 2
print(sum([h['previous_value'] for h in histories]))



