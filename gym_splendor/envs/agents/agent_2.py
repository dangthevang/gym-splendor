from ..base.player import Player

class Agent(Player):
  def action(self, state):
      stocks = []
      card = None
      stock_return = []
      return state,stocks,card,stock_return
