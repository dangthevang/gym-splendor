from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None, SAS= None):
        print(len(SAS['ListState']), len(SAS["ListAction"]))
        if SAS["Win"]==True:
            print(self.name, state['Turn'], self.score)
        t = SAS["ListAction"][random.randint(1,len(SAS["ListAction"])-1)]
        return t