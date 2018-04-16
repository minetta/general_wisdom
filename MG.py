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
#  ·   Wolframe celluar encoding trick is engaged.
#  ·
#  ===============================================

# use my default iPython imports

class Agent():
    def __init__(self, nmem=4, nstrategy=100):
        # choose strategies for this Agent (chose without placeback):
        # NOTE:
        #   a string with length 2^m corresponds to a specific strategy.
        #   This is the similar trick used in Wolframe celluar automata.
        self.Strategy_Array = list(set([
                                ''.join(str(randint(2)) for _ in range(2**nmem))
                                for _ in range(nstrategy)
                                ]))
        #
        # how many times this strategy would win
        self.Strategy_Score = zeros([len(self.Strategy_Array)])
        #
        self.tstate = 0  # which strategy this Agent use now
        self.lstact = 0  # action this Agent took at the previous iteration
        self.wtimes = 0  # how many wins this Agent obtained


    def action(self, mstate):
        # mstate: state of memory
        # now choose the best strategy,  and set self.tstate
        maxscore = max(self.Strategy_Score)
        #  avoid always using the 1st highest score strategy
        idx = rlen(self.Strategy_Score)
        shuffle(idx)
        for i in idx:
            if self.Strategy_Score[i] == maxscore:
                self.tstate = i
                break
        #
        cur_stratg = self.Strategy_Array[self.tstate]
        self.lstact = int(cur_stratg[mstate], 2)
        return self.lstact


    def update(self, mstate, wstate):
        # wstate: win state
        self.wtimes += int(self.lstact == wstate)
        # update score of each strategy,
        # according to its lose/win at this iteration:
        for i,x in enumerate(self.Strategy_Array):
            dscore = sign(int(x[mstate] == wstate)-0.5) # 0,1 -> -1,1
            self.Strategy_Score[i] += dscore


class World():
    def __init__(self, nagent=1000, nstep=1000, nmem=4, nstrategy=100):
        self.nstrategy = nstrategy # number of strategies for each user
        self.nmem = nmem # memory length
        self.mem = randint(2**self.nmem)  # info before runing!
        # new info is stored in the lowest/right bit
        self.nstep = nstep # number of steps in this launch/run
        self.nagent = nagent # number of Agents
        self.agents = [Agent(self.nmem, self.nstrategy)
                        for _ in range(self.nagent)] #initialize Agents
        self.winner = 0 # which group wins at this iteration?
        self.win_hist = [] # record winner at each iteration
        self.mem_hist = [] # record memory at each iteration


    def run(self):
        for stp in range(self.nstep):
            # collect ask and bids:
            total_action = 0
            for agt in self.agents:
                total_action += agt.action(self.mem)
            #
            # dealmaking & updating:
            self.winner = 1 if total_action<0.5*self.nagent else 0
            self.win_hist.append(self.winner)
            self.mem_hist.append(self.mem)
            self.mem = mod(self.mem*2 + self.winner, 2**self.nmem)
            #
            # account-clearance:
            for agt in self.agents:
                agt.update(self.mem, self.winner)
