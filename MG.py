#  !/usr/bin/env python
#  -*- coding:utf-8 -*-

#  ===============================================
#  ·
#  · Author: A Wang
#  ·
#  · Albert.mj.wang@gmail.com
#  ·
#  · Filename: MG.py
#  ·
#  · COPYRIGHT 2018
#  ·
#  · Describe:
#  ·   This is the basic frame and implementation
#  ·   of the traditional MG by Prof YC Zhang etc.
#  ·
#  ===============================================

class Agent():
    def __init__(self, nmem=4, nstrategy=2):
        # choose strategies represented by strings with length 2^m
        self.Strategy_Array = array(list(set([''.join(str(randint(2)) for _ in range(2**nmem)) for _ in range(nstrategy)])))
        # NOTE: len(self.Strategy_Array)<=nstrategy here, however it should be ==
        self.Strategy_Score = zeros([len(self.Strategy_Array)])
        self.lstact = randint(2)  # action this Agent would take
        self.wtimes = 0  # how many wins this Agent obtained


    def action(self, mstate):
        # randomly choose the best strategy and return action
        idx = self.Strategy_Score >= max(self.Strategy_Score)
        strgy = choice(self.Strategy_Array[idx])
        self.lstact = int(strgy[mstate], 2)
        return self.lstact


    def update(self, mstate, wstate):
        # update this agent's winned times
        self.wtimes += int(self.lstact == wstate)
        # update score of each strategy+-1, according to its lose/win:
        dScore = array([sign(int(strgy[mstate]==wstate)-0.5) for strgy in self.Strategy_Array])
        self.Strategy_Score += dScore


class World():
    def __init__(self, nagent=1000, nstep=10000, nmem=4, nstrategy=2):
        self.nstrategy = nstrategy # number of strategies for each user
        self.nmem = nmem # memory length
        self.wstate_hist = [randint(2) for _ in range(2**nmem)] # winned states
        self.wstate = self.wstate_hist[-1] # which group wins at this iteration?
        self.mstate = int(''.join(str(x) for x in self.wstate_hist[-nmem:]), 2) # mem state
        self.nstep = nstep # number of steps in this launch/run
        self.nagent = nagent # number of Agents
        self.agents = [Agent(nmem, nstrategy) for _ in range(nagent)] # Agents
        self.ACTION_hist = [] # record total action at each iteration
        self.winnum_hist = [] # how many agents winned at each iteration?
        self.prices_hist = [0] # record prices at each iteration


    def run(self):
        # take each iteration
        for stp in range(self.nstep):
            # collect ask and bids:
            total_action = sum([agt.action(self.mstate) for agt in self.agents])
            # dealmaking:
            self.wstate = randint(2) if (total_action==0.5*self.nagent) else (1  if (total_action< 0.5*self.nagent) else 0)
            self.wstate_hist.append(self.wstate)
            # account-clearance:
            for agt in self.agents: agt.update(self.mstate, self.wstate)
            # updating:
            self.mstate = int(''.join(str(x) for x in self.wstate_hist[-self.nmem:]), 2) # mem state
            self.prices_hist.append(self.prices_hist[-1] + sign(self.wstate-0.5)*(total_action/self.nagent))
            self.ACTION_hist.append(total_action)
            self.winnum_hist.append(total_action if total_action<=0.5*self.nagent else (self.nagent-total_action))
