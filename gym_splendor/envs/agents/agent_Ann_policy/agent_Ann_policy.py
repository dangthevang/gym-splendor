from ...base.player import Player
import random
from copy import deepcopy
import numpy as np

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        self.get_state(state)
        return [], None, []

    def get_state(self, state):
        state = ''
        board_stocks = state['Board'].stocks.copy()
        print(board_stocks)