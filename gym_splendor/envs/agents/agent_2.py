from ..base.player import Player
import random
import math
import json
from itertools import combinations,product
import numpy as np
import pathlib


def find_possible_actions(board_materials,hand_materials):
    actions_possible = []
    for lay in range(1,4):
        nl_lay = list(combinations(board_materials, lay))
        for bo_nl in nl_lay:
            set_tren_tay = set(hand_materials)
            set_dinh_lay = set(list(bo_nl))
            nl_con_lai = set_tren_tay.difference(set_dinh_lay)
            nl_bo = list(product(nl_con_lai,repeat= (min(len(list(bo_nl)),5-len(list(bo_nl))))))
            for poss in nl_bo:
                actions_possible.append([list(bo_nl),list(poss)])
    nl_lay = list(combinations(board_materials, 1))
    for nl in nl_lay:
        setA = set(board_materials)
        setB = set(list(nl))
        nl_con_lai = setA.difference(setB)
        nl_bo = list(product(nl_con_lai,repeat=2))
        for poss in nl_bo:
            actions_possible.append([list(nl)+list(nl),list(poss)])
    return actions_possible

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
        f = open("./gym_splendor/envs/agents/data.json")
        self.act_possible = json.load(f)
        f = open("./gym_splendor/envs/agents/mind.json")
        self.mind = json.load(f)
        self.s_a_pair = []
        f = open("./gym_splendor/envs/agents/point_act.json")
        self.point_act = json.load(f)



    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        # các action có thể làm
        hand = []
        board = []
        for nl in state["Board"].stocks.keys():
            if state["Board"].stocks[nl] >0 and nl != "auto_color":
                board.append(nl)
        for nl in self.stocks.keys():
            if self.stocks[nl] > 0 and nl != "auto_color":
                hand.append(nl)
        act_can_do = find_possible_actions(board,hand)
        if len(self.card_upside_down) == 3:
            for the in state["Board"].dict_Card_Stocks_Show["I"]:
                if self.check_get_card(the):
                    act_can_do.append([the.id,[]])
            for the in state["Board"].dict_Card_Stocks_Show["II"]:
                if self.check_get_card(the):
                    act_can_do.append([the.id,[]])
            for the in state["Board"].dict_Card_Stocks_Show["III"]:
                if self.check_get_card(the):
                    act_can_do.append([the.id,[]])
        else:
            for nl in hand:
                for the in state["Board"].dict_Card_Stocks_Show["I"]:
                    act_can_do.append([the.id,[nl]])
                for the in state["Board"].dict_Card_Stocks_Show["I"]:
                    act_can_do.append([the.id,[nl]])
                for the in state["Board"].dict_Card_Stocks_Show["I"]:
                    act_can_do.append([the.id,[nl]])
        if len(act_can_do) == 0:
            return [],None,[]
        # action
        act = random.choices(act_can_do)[0]
        # act_id = self.act_possible.index(act)
        main_act = act[0]
        sub_act = act[1]
        stock_return = sub_act
        if main_act[0] == "I":
            for the in state["Board"].dict_Card_Stocks_Show["I"]:
                if the.id == main_act:
                    card = the
            for the in state["Board"].dict_Card_Stocks_Show["II"]:
                if the.id == main_act:
                    card = the
            for the in state["Board"].dict_Card_Stocks_Show["III"]:
                if the.id == main_act:
                    card = the
        else:
            stocks = main_act
        return stocks, card, stock_return
    


