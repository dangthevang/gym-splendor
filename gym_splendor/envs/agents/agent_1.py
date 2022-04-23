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
        f = open("/content/gym-splendor/gym_splendor/envs/agents/data.json")
        self.act_possible = json.load(f)
        f = open("/content/gym-splendor/gym_splendor/envs/agents/mind.json")
        self.mind = json.load(f)
        self.s_a_pair = []
        f = open("/content/gym-splendor/gym_splendor/envs/agents/point_act.json")
        self.point_act = json.load(f)



    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        # tạo state
        observed = []
        for nl in state["Board"].stocks.values():
            observed.append(nl)
        for nl in self.stocks.values():
            observed.append(nl)
        for nl in self.stocks_const.values():
            observed.append(nl)
        observed.append(self.score)
        cards = []
        for _ in range(100):
            cards.append(0)
        # print(cards)
        for type_card in state["Board"].dict_Card_Stocks_Show.keys():
            for card in state["Board"].dict_Card_Stocks_Show[type_card]:
                countI = card.id.count("I")
                new_id = -1
                if countI == 2:
                    new_id = 39
                if countI == 3:
                    new_id = 69
                if type_card == "Noble":
                    new_id = 89
                thutu = card.id[card.id.index("_")+1:]
                new_id += int(thutu)
                cards[new_id] = 1
        observed += cards
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
        # weight map
        weighted_map = np.zeros(len(self.act_possible))
        for id in range(len(observed)):
            name = str(id) + "_" +str(observed[id])
            if name not in self.mind:
                weighted_new = np.ones(len(self.act_possible))*100
                self.mind[name] = list(weighted_new)
            else:
                weighted_new = np.array(self.mind[name])
            weighted_map += weighted_new
        weight_can_do = []
        priority = None
        max_score = 0
        for act in act_can_do:
            weight_can_do.append(weighted_map[self.act_possible.index(act)])
            score = self.point_act[self.act_possible.index(act)]
            if score > max_score:
                max_score = score
                priority = act
        # action
        # tìm action ưu tiên
        if priority == None:
        # nếu không có action ưu tiên
            act = random.choices(act_can_do,weights= weight_can_do)[0]
        act_id = self.act_possible.index(act)
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
        self.s_a_pair.append([observed,act_id])
        return stocks, card, stock_return
    
