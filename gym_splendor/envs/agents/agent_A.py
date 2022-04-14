from ..base.player import Player
import random
import math

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):

        # dict_keys(['name', 'max_init_stock', '_Board__stocks', '_Board__dict_Card_Stocks_Show', '_Board__dict_Card_Stocks_UpsiteDown'])
        
        # red blue green white black auto

        # sdict_keys(['_Card__score', '_Card__stocks', '_Card__id', '_Card_Stock__type_stock'])

        # dict_keys(['_Card__score', '_Card__stocks', '_Card__id'])

        # dict_keys(['message', '_Player__name', '_Player__score', '_Player__stocks', '_Player__stocks_const', '_Player__card_open', '_Player__card_upside_down', '_Player__card_noble'])

        stocks = []
        card = None
        stock_return = []

        stocks = ['red']

        return stocks, card, stock_return