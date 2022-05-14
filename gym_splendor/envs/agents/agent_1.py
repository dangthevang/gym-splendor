from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None,action_space = None):
        stocks = []
        card = None
        stock_return = []
        print(action_space)
        return stocks, card, stock_return
    