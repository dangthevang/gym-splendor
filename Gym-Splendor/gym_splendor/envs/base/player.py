class Player:
    def __init__(self, name):
        self.message = ""
        self.__name = name
        self.__score = 0
        self.__stocks = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0,
            "auto_color": 0,
        }
        self.__stocks_const = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0,
        }
        self.__card_open = []
        self.__card_upside_down = []
        self.__card_noble = []
# Name

    @property
    def name(self):
        return self.__name

    def setName(self, value):
        self.__name = value
# Score

    @property
    def score(self):
        return self.__score

    @score.setter
    def setScore(self, value):
        self.__score = value
# Stock

    @property
    def stocks(self):
        return self.__stocks.copy()

    @stocks.setter
    def setStocks(self, value):
        self.__stocks = value
# Stocks Const

    @property
    def stocks_const(self):
        return self.__stocks_const.copy()

    @stocks_const.setter
    def setStocks_const(self, value):
        self.__stocks_const = value
# card_open

    @property
    def card_open(self):
        return self.__card_open

    @card_open.setter
    def setCard_open(self, value):
        self.__card_open = value
# card_upside_down

    @property
    def card_upside_down(self):
        return self.__card_upside_down

    @card_upside_down.setter
    def setCard_open(self, value):
        self.__card_upside_down = value
# card_noble

    @property
    def card_noble(self):
        return self.__card_noble

    @card_noble.setter
    def setCard_noble(self, value):
        self.__card_noble = value

    def action_space(self, state, stocks=[], card=None, stock_return=[]):
        if len(stocks) != 0:
            if self.check_input_stock(stocks) == 1:
                for stock in stocks:
                    self.__stocks[stock] += 1
            elif self.check_input_stock(stocks) == 2:
                self.__stocks[stocks[0]] += 2
            else:
                print("Không thể lấy thẻ do đầu vào bị lỗi!!!")
            self.return_stock(state, stock_return)
        else:
            if self.check_get_card(card):
              self.get_card(self, state, card)
            elif self.check_upsite_down():
              self.get_upside_down(self,state, card)
              self.return_stock(state, stock_return)
        return state

    def validate_stock(self, arr_stock):
        '''
        0: arr_stock bi loi khong dung dinh dang
        1: lay 1,2,3 loai nguyen lieu
        2: lay 2 cua loai 1 nguyen lieu
        '''
        amount_stock = len(arr_stock)
        types_stock = len(list(set(arr_stock)))
        scale = amount_stock/types_stock
        if "auto_color" in arr_stock:
            print("Lỗi đầu vào lấy stock auto_color")
            return 0
        if amount_stock > 3 or scale == 3 or scale == 1.5:
            print("Lỗi đầu vào lấy không đúng số lượng loại, hoặc số lượng stock")
            return 0
        if scale == 1:
            return 1
        if scale == 2:
            return 2

    def check_input_stock(self, arr_stock, state):
        if self.validate_stock(self, arr_stock) == 1:
            for stock in arr_stock:
                if state["Board"].stocks[stock] == 0:
                    print("Không đủ điều kiện trên bàn")
                    return 0
            return 1
        if self.validate_stock(self, arr_stock) == 2:
            if state["Board"].stocks[arr_stock[0]] <= len(state["Agent"])//2:
                print("Không đủ điều kiện trên bàn")
                return 0
            return 2

    def return_stock(self, state, stock_return):
        if sum(self.__stocks.values()) > 10:
            if len(stock_return) >= sum(self.__stocks.values()) - 10 and self.check_return(stock_return):
                for stock in stock_return:
                    self.__stocks[stock] = self.__stocks[stock] - 1
                return state["Board"].postStock(stock_return)
            else:
                print(
                    " Số lượng thẻ bỏ chưa đúng hoặc số thẻ trả bị âm, Cần sửa lại ngay")
        return

    def check_get_card(self, Card):
        auto_color = self.__stocks["auto_color"]
        for i in Card.stocks.keys():
            if self.__stocks[i] + self.__stocks_const[i] < Card.stocks[i]:
                if self.__stocks[i] + self.__stocks_const[i] + auto_color >= Card.stocks[i]:
                    auto_color = self.__stocks[i] + \
                        self.__stocks_const[i] + auto_color - Card.stocks[i]
                else:
                    return False
        return True

    def check_return(self, stock_return):
        stock_current = self.stocks
        for stock in stock_return:
            stock_current[stock] -= 1
            if stock_current[stock] < 0:
                return False
        return True

    def get_upside_down(self,state, Card, stock_return):
            auto_color = 0
            if state["Board"].stocks["auto_color"] >= 1:
                auto_color = 1
                self.__stocks["auto_color"] += 1
            # -------
            a = self.getPositionCard(state["Board"], Card)
            show = a["show"]
            key = a["key"]
            if show == True:
                self.__card_upside_down.append(Card)
                state["Board"].deleteUpCard(key, Card)
            else:
                self.__card_upside_down.append(
                  state["Board"].dict_Card_Stocks_UpsiteDown[key][1])
                state["Board"].deleteCardInUpsiteDown(
                  key, state["Board"].dict_Card_Stocks_UpsiteDown[key][1])
            state["Board"].getStock({"auto_color": auto_color})

    def get_card(self, state, Card):
        stock_return = {"red": 0,
                        "blue": 0,
                        "green": 0,
                        "white": 0,
                        "black": 0,
                        "auto_color": 0, }
        self.__card_open.append(Card)
        self.__score += Card.score
        for i in Card.stocks.keys():
            stocks_late = self.__stocks[i]
            if stocks_late + self.__stocks_const[i] < Card.stocks[i]:
                auto_color = self.__stocks["auto_color"]
                self.__stocks["auto_color"] = self.__stocks["auto_color"] - (Card.stocks[i] - self.__stocks[i] -
                                                                             self.__stocks_const[i])
                self.__stocks[i] = self.__stocks[i] + (
                    auto_color-self.__stocks["auto_color"]) + self.__stocks_const[i] - Card.stocks[i]
                stock_return["auto_color"] = auto_color - \
                    self.__stocks["auto_color"]
                stock_return[i] = stocks_late
            else:
                if self.__stocks_const[i] >= Card.stocks[i]:
                    stock_return[i] = 0
                else:
                    self.__stocks[i] = stocks_late + \
                        self.__stocks_const[i] - Card.stocks[i]
                    stock_return[i] = stocks_late - self.__stocks[i]
        self.__stocks_const[Card.type_stock] += 1

        a = self.get_position_card(state, Card)
        mine = a["mine"]
        if mine == False:
            state["Board"].deleteUpCard(a["key"], Card)
        else:
            self.__card_upside_down.remove(Card)
        state["Board"] = self.getNoble(state["Board"])
        state["Board"].postStock(stock_return)
        return state

    def get_position_card(self, state, card):
        for i in self.__card_upside_down:
            if i.id == card.id:
                return {
                    "mine": True,
                }
        for i in state["Board"].dict_Card_Stocks_Show.keys():
            for j in state["Board"].dict_Card_Stocks_Show[i]:
                if j.id == card.id:
                    return{
                        "key": i,
                        "mine": False,
                        "show": True,
                    }
        for i in state["Board"].dict_Card_Stocks_UpsiteDown.keys():
            for j in state["Board"].dict_Card_Stocks_UpsiteDown[i]:
                if j.id == card.id:
                    return{
                        "key": i,
                        "show": False,
                    }

# Lấy thẻ Quý tộc nếu có thể
    def getNoble(self, state):
        b = []
        for card_Noble in state["Board"].dict_Card_Stocks_Show["Noble"]:
            check = True
            for i in card_Noble.stocks.keys():
                if self.__stocks_const[i] < card_Noble.stocks[i]:
                    check = False
            b.append(check)
        for i in range(len(b)):
            if b[i] == True:
                card_Noble = state["Board"].dict_Card_Stocks_Show["Noble"][i]
                self.__score += card_Noble.score
                self.__card_noble.append(card_Noble)
        for i in self.__card_noble:
            try:
                state["Board"].deleteCardNoble(i)
            except:
                continue
    def check_upsite_down(self):
      if len(self.__card_upside_down) < 3:
          return True
      else:
          return False
        


# Kiểm tra xem có lấy được 3 nguyên liệu hay không

    def checkThreeStocks(self, board, color_1, color_2, color_3):
        try:
            if color_1 == "auto_color" or color_2 == "auto_color" or color_3 == "auto_color":
                return False
            if color_1 == color_2 or color_1 == color_3 or color_2 == color_3:
                return False
            if board.stocks[color_1] == 0:
                return False
            elif board.stocks[color_2] == 0:
                return False
            elif board.stocks[color_3] == 0:
                return False
            return True
        except AttributeError:
            error.errorColor(
                "Check Three Stocks Có tham số nào đó truyền vào bị rỗng nên không thực hiện được hàm")
            return False

# Kiểm tra xem có lấy được 1 nguyên liệu hay không
    def checkOneStock(self, board, color_1):
        try:
            if color_1 == "auto_color":
                return False
            if board.stocks[color_1] <= 3:
                return False
            return True
        except AttributeError:
            error.errorColor(
                "Check One Stocks  Có tham số nào đó truyền vào bị rỗng nên không thực hiện được hàm")
            return False
