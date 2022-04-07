from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stocks_return = []
        stocks = ["red","red"]
        stocks_return = ["red"]
        return stocks,card,stocks_return
