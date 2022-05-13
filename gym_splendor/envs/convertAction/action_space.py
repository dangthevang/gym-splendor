from gym_splendor.envs.convertAction import convert as cv
import pandas as pd
def amount(*arg):
  count = 0
  for i in arg:
    if i != "0":
      count +=1
  return count
def IndexPlayer(state,player):
  for i in range(len(state["Player"])):
    if player.stt == state["Player"][i].stt:
      return i

class Action_Space_State():
    def __init__(self):
        self.all_action = pd.read_json("gym_splendor/envs/data_action/action_space.json", orient="index")
        self.list_state = []
    def clone_all_action(self):
      return self.all_action.copy()
    def process(self):
        self.all_action["amount_stock"] = self.all_action.apply(lambda row: amount(row["Stock1", "Stock2", "Stock3"]),axis=1)
        self.all_action["amount_stock_return"] = self.all_action.apply(lambda row: amount(row["StockReturn1", "StockReturn2", "StockReturn3"]),axis=1)
    def recomend_action(self,state,player):
        data = pd.DataFrame(columns = ["TypeAction","Stock1","Stock2","Stock3","Card","StockAutoColor","StockReturn1","StockReturn2","StockReturn3"])
        stock_board = state["Board"].stocks
        stock_player = player.stocks
        list_get_stock = list(cv.FilterColor(stock_board,Return_=False))
        list_push_stock = list(cv.FilterColor(stock_player,Return_=True))

        for s in list_get_stock:
          for r_s in list_push_stock:
            if len(s) >= len(r_s) and cv.compare(s,r_s) == 0  and sum(player.stocks.values())+len(s)-len(r_s)<=10:
              data = data.append(cv.formatGetStock(s,r_s),ignore_index=True)
        
        for card in state["Board"].getCardUp():
          id = cv.to_str(card.stt)
          if player.check_get_card(card):
            data = data.append(cv.getCard(id),ignore_index=True)
          if stock_board["auto_color"]>0:
            data = data.append(cv.getUpDown(id),ignore_index=True)
          else:
            data = data.append(cv.getUpDownNoneAuto(id),ignore_index=True)
        data = cv.CreateCode(data)
        data["check"] = [True for i in data["CodeAction"]]
        df = self.clone_all_action()
        df = df.merge(data[["CodeAction","check"]],how='left',on='CodeAction')
        return df[df["check"]==True].index

    def covertState(self,state,player):
      self.list_state = []
      for value in state["Board"].stocks.values():
        self.list_state.append(value)
      list_card = self.formatListCard(state["Board"].getCardUp("Noble"))
      for i in list_card:
        self.list_state.append(i)
      index = IndexPlayer(state,player)
      for i in range(index, index+4):
        vitri = i % len(state["Player"])
        for value in state["Player"][vitri].stocks.values():
          self.list_state.append(value)
        for value in state["Player"][vitri].stocks_const.values():
          self.list_state.append(value)
        list_card = self.formatListCard(state["Player"][vitri].card_open)
        for i in list_card:
          self.list_state.append(i)
        if i == index:
          list_card = self.formatListCard(state["Player"][vitri].card_upside_down)
          for i in list_card:
            self.list_state.append(i)
        list_card = self.formatListCard(state["Player"][vitri].card_noble)
        for i in list_card:
          self.list_state.append(i)
      return self.list_state


    def formatListCard(self,arr):
      list_card = [0 for i in range(0,100)]
      for card in arr:
        list_card[card.stt-1] = 1
      return list_card



    




