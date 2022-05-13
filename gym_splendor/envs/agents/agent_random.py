from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None, SAS= None):
        # print(SAS["ListState"])
        t = SAS["ListAction"][random.randint(1,len(SAS["ListAction"])-1)]
        return t