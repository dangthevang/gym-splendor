from re import T
from ..base.player import Player
import random
import math
import json
import numpy as np


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None):
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        number = random.randint(0,len(a)-1)
        try:
            s_a = pd.read_csv('State_tam_2.csv')
        except:
            s_a = pd.DataFrame({'state':[], 'action': [], 'list_action':[], 'win': []})
        
        s_a = pd.concat([s_a, pd.DataFrame({'state':t, 'action': number, 'list_action':a, 'win': []})])
        s_a.to_csv('State_tam_2.csv')
        return a[number]
