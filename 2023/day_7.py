#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
#%%
import re
import logging
from enum import IntEnum

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

##
#%%

def get_lines(test=False):
    """ reads lines from string or input file and returns an array """
    if test:
        # small string input for initial testing
        string = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

        lines = [l.strip() for l in string.splitlines()]

    else:
        # getting lines from input file
        with open('2023/day_7.input', 'r') as file:
            lines = file.readlines()

    return [l.strip() for l in lines]


logger.debug(get_lines(test=True))

##
#%%

strengths = { 'A':14, 'K':13, 'Q':12, 'J':11, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2': 2}

class Type(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

types = {7: 'Five of a kind',
         6: 'Four of a kind',
         5: 'Full house',
         4: 'Three of a kind',
         3: 'Two pair',
         2: 'One pair',
         1: 'High card'}

def get_type(hand_dict):
    counts = list(hand_dict.values())
    if 5 in counts:
        return Type.FIVE_OF_A_KIND
    if 4 in counts:
        return Type.FOUR_OF_A_KIND
    if (3 in counts) and (2 in counts):
        return Type.FULL_HOUSE
    if 3 in counts:
        return Type.THREE_OF_A_KIND
    if sum([n == 2 for n in counts]) == 2:
        return Type.TWO_PAIR
    if 2 in counts:
        return Type.ONE_PAIR
    return Type.HIGH_CARD

def hand_score(hand_type, hand_str, strengths=strengths):
    score = hand_type.value
    for c in hand_str:
        score = score * 100 + strengths[c]
    return score

##
#%%

sep_pattern = "\s+"
sep_prog = re.compile(sep_pattern)

def read_lines(lines):
    hands = []
    for line in lines:
        logger.debug(f"line: {line}")
        hand_str, bid_str = sep_prog.split(line)
        hand_dict = {}
        for c in hand_str:
            hand_dict[c] = hand_dict.get(c, 0) + 1
        type = get_type(hand_dict)
        score = hand_score(type, hand_str)
        hand = {"str": hand_str,
                "dict": hand_dict,
                "bid": int(bid_str),
                "type": type,
                "score": score
                }
        hands.append(hand)
        logger.debug(hand)

    return hands

logger.debug(read_lines(get_lines(test=True)))

##
#%%


##
#%%

def compute_result(sorted_hands):
    result = 0
    for idx, hand in enumerate(sorted_hands):
        rank = idx + 1
        hand['rank'] = rank
        result += rank * hand['bid']
        logger.debug(hand)
    return result

##
#%

# Part 1
hands = read_lines(get_lines(test=False))
hands.sort(reverse=False, key=lambda i: i['score'])

print(compute_result(hands))

##
#%%

# Part 2

strengths_2 = { 'A':14, 'K':13, 'Q':12, 'J':1, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2': 2}

def enrich_hands(hands):
    for hand in  hands:
        logger.debug(hand)
        hand_dict_2 = {k:v for k,v in hand['dict'].items() if k != 'J'}
        if len(hand_dict_2) == 0:
            # in case of "JJJJJ"
            hand_dict_2['A'] = 5
        else:
            best_card = max([ (v, k) for k,v in hand_dict_2.items()])[1]
            hand_dict_2[best_card] += hand['dict'].get('J', 0)
        type_2 = get_type(hand_dict_2)
        score_2 = hand_score(type_2, hand['str'], strengths=strengths_2)
        hand['dict_2'] = hand_dict_2
        hand['type_2'] = type_2
        hand['score_2'] = score_2
        logger.debug(f"{hand['dict']} , {hand_dict_2}")


##
#%%
hands = read_lines(get_lines(test=False))
enrich_hands(hands)
hands.sort(reverse=False, key=lambda i: i['score_2'])

print(compute_result(hands))
