import json
learn = open('test/NA.json')
learning = json.load(learn)

action = json.load(open('test/data_action.json'))
for i in action:
    print(i)


import json
import random
import gym
from matplotlib.pyplot import close

from gym_splendor.envs.base.board import Board
from gym_splendor.envs.base.card import Card_Stock,Card_Noble
from gym_splendor.envs.agents import agents_inteface
from gym_splendor.envs.base import error

def getType(dict_type):
        for j in dict_type.keys():
            if dict_type[j] == 1:
                return j
amount_player = 4
class SplendporEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.turn = 0
        self.amount_player = amount_player
        self.board = None
        self.player = None
        self.pVictory = None
        self.state = {}
        # self.render()

    def step(self, action):
        if self.close() and self.turn % self.amount_player == 0:
            # print("**********************************************************************************************************")
            return self,None,True,None
        else:
            stocks = action[0]
            card = action[1]
            stock_return = action[2]
            # print("**********************************************************************************************************")
            error.errorColor(str(self.turn % self.amount_player))
            self.state["Turn"] = self.turn+1
            self.player[self.turn % self.amount_player].action_space(self.state,stocks,card,stock_return)
            self.turn = self.turn+1
        return self.state,None,None,None


    def reset(self):
        self.turn = 0
        self.amount_player = amount_player
        self.board = Board()
        self.player = random.sample(agents_inteface.ListPlayer, k=self.amount_player)
        for p in self.player:
            p.reset()
        self.pVictory = None
        self.state = {
            "Turn" : 0,
            "Board": self.board,
            "Player": self.player,
        }
        self.setup_board()

    def render(self, mode='human', close=False):
        print("Turn", self.turn, "Board Stocks",self.board.stocks)
        self.board.hien_the()
        # print("Board Stocks",self.board.stocks)
        t = 0
        for p in self.player:
            print(p.name,p.score,list(p.stocks.values()),list(p.stocks_const.values()),end="")
            # print(" Card got: ",end="")
            # for i in p.card_open:
            #     print(i.id, end=" ")
            t +=1
            if t % 2 == 0:
                print()
            else:
                print(end="    ")
        print("----------------------------------------------------------------------------------------------------------")

    def setup_board(self):
        self.board.Stocks(self.amount_player)
        with open('gym_splendor/envs/Cards_Splendor.json') as datafile:
            data = json.load(datafile)
        Ma = ""
        stt = 1
        dict_board_board_show = { 'I': [],
            'II': [],
            'III': [],
            'Noble': []}
        dict_board_upsite_down = { 'I': [],
            'II': [],
            'III': [],
            'Noble': []}
        for i in data:
            if stt <= 40:
                Ma = "I_" + str(stt)
            elif stt <= 70:
                Ma = "II_" + str(stt - 40)
            elif stt <= 90:
                Ma = "III_" + str(stt - 70)
            else : 
                Ma = "Noble_"+ str(stt - 90)
            stt+=1
            if i["type"] != "Noble":
                c = Card_Stock(Ma,
                    getType(i["type_stock"]), i["score"], i["stock"])
                dict_board_upsite_down[i["type"]].append(c)
            else:
                c = Card_Noble(Ma,i["score"], i["stock"])
                dict_board_upsite_down["Noble"].append(c)
        for i in dict_board_upsite_down.keys():
            random.shuffle(dict_board_upsite_down[i])

        for key in dict_board_board_show.keys():
            for i in range(4):
                dict_board_board_show[key].append(dict_board_upsite_down[key][0])
                dict_board_upsite_down[key].remove(dict_board_upsite_down[key][0])
        dict_board_board_show["Noble"].append(dict_board_upsite_down["Noble"][0])
        dict_board_upsite_down["Noble"].remove(dict_board_upsite_down["Noble"][0])
        self.state["Board"].setDict_Card_Stocks_Show(dict_board_board_show)
        self.state["Board"].setDict_Card_Stocks_UpsiteDown(dict_board_upsite_down)

    def close(self):
        arr_point = [i.score for i in self.player]
        max_point = max(arr_point)
        if max_point >= 15:
            arr_point = [1 if i == max_point else 0 for i in arr_point]
            arr_amount_card = [len(i.card_open) for i in self.player]
            min = 100
            for i in range(len(arr_point)):
                if arr_point[i] == 1 and arr_amount_card[i] < min:
                    min = arr_amount_card[i]
                    self.pVictory = self.player[i]
            return True
        return False


import gym
import gym_splendor
import os
import pandas as pd


def check_winner(state):
    name = ''
    score_max = 14
    player_win = None
    if state['Turn']%4 == 0:
        for player in list(state['Player']):
            if player.score > score_max:
                score_max = player.score 
        if score_max > 14:
            for player in list(state['Player']):
                if player.score >= score_max:
                    score_max = player.score 
                    player_win = player
                elif player.score == score_max:
                    if len(player.card_open) < len(player_win.card_open):
                        player_win = player
    if player_win != None:
        return player_win.name, score_max, 'ở turn ' + str(int(state['Turn']/4))
    else:
        return "NA0"

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <150:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break
    state = env.state
    print(check_winner(state))

if __name__ == '__main__':
    main()

