#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:12:25 2024

@author: glg
"""

import re

import pprint

pp = pprint.PrettyPrinter(depth=6)

test_string = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

colors = ['red', 'blue', 'green']
color_pattern = "|".join(colors)

#%% 


test_string = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
print(f"string: {test_string}")
#test_string = "Game 1: "
pattern = "Game\s\d:(\s(\d)\s(" + color_pattern + "),?)+"
#pattern = "Game\s\d:\s\d\s(blue|red|green)" #(red)|(blue)|(green)"
pattern_game = "Game\s(\d):(.*)"
print(f"pattern: {pattern_game}")

prog_game = re.compile(pattern_game)
m_game = prog_game.match(test_string)
print(m_game)
if m_game:
    print(m_game.groups())

print()
test_string = m_game.group(2)
print(f"string: {test_string}")
pattern_draw = ";"
print(f"pattern: {pattern_draw}")

prog_draw = re.compile(pattern_draw)

split_draw = prog_draw.split(test_string)
print(split_draw)

print()
test_string = split_draw[0]
print(f"string: {test_string}")
pattern_color = ","

print(f"pattern: {pattern_color}")

prog_color = re.compile(pattern_color)

split_color = prog_color.split(test_string)
print(split_color)

print()
pattern_color = "\s*(\d)\s+(" + color_pattern + ")"
print(f"pattern: {pattern_game}")

test_string = split_color[0]
prog_game = re.compile(pattern_color)
m_color = prog_game.match(test_string)
print(m_color)
if m_game:
    print(m_color.groups())

#%%
pattern_game = r"Game\s(\d+):(.*)"
prog_game = re.compile(pattern_game)
pattern_draw_sep = ";"
prog_draw_sep = re.compile(pattern_draw_sep)
pattern_color_sep = ","
prog_color_sep = re.compile(pattern_color_sep)
pattern_color = r"\s*(\d+)\s+(" + color_pattern + ")"
prog_color = re.compile(pattern_color)


#%%

games = []
for line in test_string.splitlines():
    print(f"line: {line}")
    m_game = prog_game.match(line)
    game = {'str': line,
            'id': int(m_game.group(1)),
            'draws': []
            }
    game_str = m_game.group(2)
    for draw_str in prog_draw_sep.split(game_str):
        draw = {'str': draw_str,
                'colors': []}
        for color_str in prog_color_sep.split(draw_str):
            #print(color_str)
            m_color = prog_color.match(color_str)
            color = {'str': color_str,
                     'nb': int(m_color.group(1)),
                     'color': m_color.group(2)}
            draw['colors'].append(color)
        game['draws'].append(draw)
    games.append(game)
pp.pprint(games)



#%%

result = 0
for game in games:
    possible = True
    for draw in game['draws']:
        for color in draw['colors']:
            if (((color['nb'] > 12) and (color['color'] == 'red'))
                    or ((color['nb'] > 13) and (color['color'] == 'green'))
                    or ((color['nb'] > 14) and (color['color'] == 'blue'))):
                possible = False
                print(f"game {game['id']} impossible because of {color['str']}")
                break
    game['possible'] = possible
    if possible:
        result += game['id']

pp.pprint(games)
print(result)

#%%
#%%

games = []
with open('2023/day_2.input', 'r') as file:
    for l in file:
        line = l.strip()
        m_game = prog_game.match(line)
        game = {'str': line,
                'id': int(m_game.group(1)),
                'draws': []
                }
        game_str = m_game.group(2)
        for draw_str in prog_draw_sep.split(game_str):
            draw = {'str': draw_str,
                    'colors': []}
            for color_str in prog_color_sep.split(draw_str):
                m_color = prog_color.match(color_str)
                color = {'str': color_str,
                         'nb': int(m_color.group(1)),
                         'color': m_color.group(2)}
                draw['colors'].append(color)
            game['draws'].append(draw)
        games.append(game)

result = 0
for game in games:
    possible = True
    for draw in game['draws']:
        for color in draw['colors']:
            if (((color['nb'] > 12) and (color['color'] == 'red'))
                    or ((color['nb'] > 13) and (color['color'] == 'green'))
                    or ((color['nb'] > 14) and (color['color'] == 'blue'))):
                possible = False
                print(f"game {game['id']} impossible because of {color['str']}")
                break
    game['possible'] = possible
    if possible:
        result += game['id']

print(result)
