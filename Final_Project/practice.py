# Created by Minbiao Han and Roman Sharykin
# AI fall 2018
# Addison Dunn (awd5eg) and Connor Albrecht (ca7xf)


from __future__ import print_function
from __future__ import division

from builtins import range
from past.utils import old_div
import MalmoPython
import json
import logging
import math
import os
import random
import sys
import time
import re
import uuid
from collections import namedtuple
from operator import add
from random import *
import numpy as np
import random as random

### You should define your evaluation function here
# Inputs: pos - tuple (position of player), enemy_pos - tuple, food - array
# Output: your evaluation score
def evalfuncReflex(pos,block_pos, enemy_pos,scores,percent):
    ### YOUR CODE HERE ###
    # returns value to a tree of eval scores
    # pos = tuple(np.subtract(pos, (0.5, 0.5)))
    # enemy_pos = tuple(np.subtract(enemy_pos, (0.5, 0.5)))

    # just values i was messing with
    enemy_temp_pos=(enemy_pos[0]-.5,enemy_pos[1]-.5)
    player_temp_pos=(pos[0]-.5,pos[1]-.5)


    score = 0
    Enemy_to_dest_dist = manhattan_distance(enemy_temp_pos, block_pos)
    player_to_dest_dist = manhattan_distance(player_temp_pos, block_pos)
    dist_to_enemy = manhattan_distance(pos, enemy_pos)



    Enemy_to_dest_dist_constant= -10
    player_to_dest_dist_constant= -5
    dist_to_enemy_constant= -10




    score = Enemy_to_dest_dist_constant*Enemy_to_dest_dist + player_to_dest_dist_constant*player_to_dest_dist + dist_to_enemy_constant*dist_to_enemy

    return new_percent, score


### Implement a way for the agent to decide which way to move
# Inputs: pos - tuple (position of player), world_state, enemy_pos - tuple, food - array
# Output: direction in which to move (can be a string, int, or whatever way you want to implement it)
# def chooseAction(pos, wstate, dest_blocks, enemy_pos):
#     ### YOUR CODE HERE ###
#     illegal_moves = illegalMoves(wstate)
#     start_score, temp = evalfuncReflex(pos, enemy_pos, dest_blocks)
#     legalLST = ["right", "left", "forward", "back"]
#     left_score = -100000
#     right_score = -100000
#     forward_score = -100000
#     back_score = -100000
#     score_arr = {}
#     dir_scores = {}

#     for i in illegal_moves:
#         if i in legalLST:
#             legalLST.remove(i)
#     dir = ""
#     for j in range(0, len(legalLST)):
#         if legalLST[j] == "left":
#             left_pos = tuple(np.add(pos, (1, 0)))
#             dir_scores["left"], score_arr["left"] = evalfuncReflex(left_pos, enemy_pos, dest_blocks)
#         if legalLST[j] == "right":
#             right_pos = tuple(np.subtract(pos, (1, 0)))
#             dir_scores["right"], score_arr["right"] = evalfuncReflex(right_pos, enemy_pos, dest_blocks)
#         if legalLST[j] == "forward":
#             forward_pos = tuple(np.add(pos, (0, 1)))
#             dir_scores["forward"], score_arr["forward"] = evalfuncReflex(forward_pos, enemy_pos, dest_blocks)
#         if legalLST[j] == "back":
#             back_pos = tuple(np.subtract(pos, (0, 1)))
#             dir_scores["back"], score_arr["back"] = evalfuncReflex(back_pos, enemy_pos, dest_blocks)

#     # assumes higher score is better


#     max_value = max(dir_scores.values())
#     max_keys = [k for k, v in dir_scores.items() if v == max_value] #get the max dirs from dir_scores
#     dir = random.choice(max_keys)   #Get random direction from max vals



#     print("LEFT SCORE: ", left_score)
#     print("RIGHT SCORE: ", right_score)
#     print("FORWARD SCORE: ", forward_score)
#     print("BACK SCORE: ", back_score)
#     print("CHOSEN DIR:", dir)
#     print("DETAILS:, ", score_arr[dir])

#     print("FOOD: ", dest_blocks)



#     return dir
def choose_dest_block(pos, wstate, dest_blocks, enemy_pos,dest_block_percents):

    max_val=-100000000
    dest_blocks_scores=[]
    count=0
    choice_dest_index=-1
    for block in dest_blocks:
        dest_block_percents[count] ,evalNUm=evalfuncReflex(pos,block,enemy_pos,dest_block_percents[count])
        dest_blocks_scores.append(evalNUm)
        count=count+1
    count=0
    for val in dest_blocks_scores:
        if max_val< val:
            max_val=val
            choice_dest_index=count
        count=count+1
    return dest_block_percents, dest_blocks[choice_dest_index]
### Move the agent here
# Output: void (should just call the correct movement function)
def reflexAgentMove(agent, pos, wstate, dest_blocks, enemy_pos,dest_block_percents):
    ### YOUR CODE HERE ###
    new_dest_block_percents, target_dest = choose_dest_block(pos, wstate, dest_blocks, enemy_pos,dest_block_percents)
    if d == "right":
        moveRight(agent)
    elif d == "left":
        moveLeft(agent)
    elif d == "forward":
        moveStraight(agent)
    elif d == "back":
        moveBack(agent)

    return

### Helper methods for you to use ###

# Simple movement functions
# Hint: if you want your execution to run faster you can decrease time.sleep
def moveRight(ah):
    ah.sendCommand("strafe 1")
    time.sleep(0.1)


def moveLeft(ah):
    ah.sendCommand("strafe -1")
    time.sleep(0.1)


def moveStraight(ah):
    ah.sendCommand("move 1")
    time.sleep(0.1)


def moveBack(ah):
    ah.sendCommand("move -1")
    time.sleep(0.1)

# Used to find which movements will result in the player walking into a wall
### Input: current world state
### Output: An array directional strings
def illegalMoves(world_state):
    blocks = []
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'floor3x3W', 0)
        if grid[3] == u'diamond_block':
            blocks.append("right")
        if grid[1] == u'diamond_block':
            blocks.append("back")
        if grid[5] == u'diamond_block':
            blocks.append("left")
        if grid[7] == u'diamond_block':
            blocks.append("forward")

        return blocks

# Used to find the Manhattan distance between two tuples
def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)

# Do not modify!
###
###
# This functions moves the enemy agent randomly #
def enemyAgentMoveRand(agent, ws):
    time.sleep(0.1)
    illegalgrid = illegalMoves(ws)
    legalLST = ["right", "left", "forward", "back"]
    for x in illegalgrid:
        if x in legalLST:
            legalLST.remove(x)
    y = randint(0,len(legalLST)-1)
    togo = legalLST[y]
    if togo == "right":
        moveRight(agent)

    elif togo == "left":
        moveLeft(agent)

    elif togo == "forward":
        moveStraight(agent)

    elif togo == "back":
        moveBack(agent)

