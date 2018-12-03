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
def evalfuncReflex(pos, enemy_pos, dest_blocks):
    ### YOUR CODE HERE ###
    # returns value to a tree of eval scores
    # pos = tuple(np.subtract(pos, (0.5, 0.5)))
    # enemy_pos = tuple(np.subtract(enemy_pos, (0.5, 0.5)))

    # just values i was messing with
    enemy_weight = -100.0
    dest_dist_weight = 150.0
    num_dest_weight = 1500.0

    score = 0
    dest_num = len(dest_blocks)
    pos_minus = tuple(np.subtract(pos, (0.5, 0.5)))
    nearest_dest_dist = manhattan_distance(pos_minus, dest_blocks[0])
    nearest_dest_index = 0
    enemy_dist = manhattan_distance(pos, enemy_pos)
    enemy_score = 0
    index_removed = -1

    # base cases
    if pos == enemy_pos:  # check if enemy is same pos, worst case
        return -100000, [0,0,0]


    # for x in range(0, dest_num):  # check if pos is food, remove food block, dec dest_num
    #     if tuple(np.subtract(pos, (0.5, 0.5))) == dest_blocks[x]:
    #     # if pos == dest_blocks[x]:
    #         dest_num -= 1
    #         break

    for i in range(1, dest_num):
        if manhattan_distance(pos_minus, dest_blocks[i]) < manhattan_distance(pos_minus, dest_blocks[nearest_dest_index]):
            nearest_dest_index = i
    nearest_dest_dist = manhattan_distance(pos_minus, dest_blocks[nearest_dest_index])

    # Enemy stuff
    enemy_score =  (enemy_weight / enemy_dist)  #weight
    num_dest_score = (num_dest_weight / dest_num)
    if nearest_dest_dist != 0:
        dest_dist_score = (dest_dist_weight / nearest_dest_dist)

    if enemy_dist <= 1:
        enemy_score = -1000

    if nearest_dest_dist == 0:
        dest_dist_score = 300
    elif nearest_dest_dist <=1:
        dest_dist_score = 200

    if nearest_dest_dist <=1 and dest_num <= 1:
        dest_dist_score = 900

    # score increases when: enemy_dist dec, num_dest inc, nearesst_dest_dist dec
    # num_dest more important than nearest_dest dist
    # main objective: get all food as fast as possible while avoiding enemy
        # so enemt_dist is less importance if not within close proximity
    # playing around with inverses and neg vs pos for food metrics
    score = dest_dist_score + num_dest_score + enemy_score
    score_arr = [dest_dist_score, num_dest_score, enemy_score, pos, dest_blocks[nearest_dest_index], nearest_dest_dist]
    # edge and base cases
        # if enemy close, high neg score
        # if food close (and enemy not as close), high pos score
    # delete food block if move towards it
    # subtract 0.5 from player for food
    # take neg. inv. of enemy dist (times some constant, 12?)
    # high weight on num food blocks left


    # enemy_dest_dist = manhattan_distance(nearest_dest_dist, enemy_pos)
    return score, score_arr


### Implement a way for the agent to decide which way to move
# Inputs: pos - tuple (position of player), world_state, enemy_pos - tuple, food - array
# Output: direction in which to move (can be a string, int, or whatever way you want to implement it)
def chooseAction(pos, wstate, dest_blocks, enemy_pos):
    ### YOUR CODE HERE ###
    illegal_moves = illegalMoves(wstate)
    start_score, temp = evalfuncReflex(pos, enemy_pos, dest_blocks)
    legalLST = ["right", "left", "forward", "back"]
    left_score = -100000
    right_score = -100000
    forward_score = -100000
    back_score = -100000
    score_arr = {}
    dir_scores = {}

    for i in illegal_moves:
        if i in legalLST:
            legalLST.remove(i)
    dir = ""
    for j in range(0, len(legalLST)):
        if legalLST[j] == "left":
            left_pos = tuple(np.add(pos, (1, 0)))
            dir_scores["left"], score_arr["left"] = evalfuncReflex(left_pos, enemy_pos, dest_blocks)
        if legalLST[j] == "right":
            right_pos = tuple(np.subtract(pos, (1, 0)))
            dir_scores["right"], score_arr["right"] = evalfuncReflex(right_pos, enemy_pos, dest_blocks)
        if legalLST[j] == "forward":
            forward_pos = tuple(np.add(pos, (0, 1)))
            dir_scores["forward"], score_arr["forward"] = evalfuncReflex(forward_pos, enemy_pos, dest_blocks)
        if legalLST[j] == "back":
            back_pos = tuple(np.subtract(pos, (0, 1)))
            dir_scores["back"], score_arr["back"] = evalfuncReflex(back_pos, enemy_pos, dest_blocks)

    # assumes higher score is better


    max_value = max(dir_scores.values())
    max_keys = [k for k, v in dir_scores.items() if v == max_value] #get the max dirs from dir_scores
    dir = random.choice(max_keys)   #Get random direction from max vals

    # if back_score > forward_score:
    #     if back_score > left_score:
    #         if back_score > right_score:
    #             dir = "back"
    #         else:
    #             dir = "right"
    #     else:
    #         if left_score > right_score:
    #             dir = "left"
    #         else:
    #             dir = "right"
    # else:
    #     if forward_score > left_score:
    #         if forward_score > right_score:
    #             dir = "forward"
    #         else:
    #             dir = "right"
    #     else:
    #         if left_score > right_score:
    #             dir = "left"
    #         else:
    #             dir = "right"

    print("LEFT SCORE: ", left_score)
    print("RIGHT SCORE: ", right_score)
    print("FORWARD SCORE: ", forward_score)
    print("BACK SCORE: ", back_score)
    print("CHOSEN DIR:", dir)
    print("DETAILS:, ", score_arr[dir])

    print("FOOD: ", dest_blocks)



    return dir

### Move the agent here
# Output: void (should just call the correct movement function)
def reflexAgentMove(agent, pos, wstate, dest_blocks, enemy_pos):
    ### YOUR CODE HERE ###
    d = chooseAction(pos, wstate, dest_blocks, enemy_pos)
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

