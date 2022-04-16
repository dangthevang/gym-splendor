import gym
import gym_splendor
import pandas as pd


def save_df(env):
    obj = env.state
    board = obj["Board"]
    player = obj["Player"]
    turn = []
    board_stocks = []
    board_hien_the = []
    player_name = []
    player_score = []
    player_stocks_values = []
    player_card_open = {}
    turn.append(obj["Turn"])
    board_stocks.append(board.stocks)
    board_hien_the.append(board.hien_the())
    t = 0
    for p in player:
        print(p.name, p.score, list(p.stocks.values()), end="")
        player_name.append(p.name)
        player_score.append(p.score)
        player_stocks_values.append(p.stocks.values())
        print(" Card got: ", end="")
        for i in p.card_open:
            if p.name in player_card_open:
                player_card_open[p.name].append(i.id)
                print(i.id, end=" ")
            else:
                player_card_open[p.name] = []
    return turn, board_stocks, player_name, player_score, player_stocks_values, player_card_open


def main():
    # env = gym.make('gym_splendor-v0')
    # env.reset()
    env = gym.make('gym_splendor-v0')
    for ban in range(10):
        env.reset()
        turn_lst = []
        board_stocks_lst = []
        player_name_lst = []
        player_score_lst = []
        player_stocks_values_lst = []
        player_card_open_lst = []

        while env.turn < 200:
            o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
            turn, board_stocks, player_name, player_score, player_stocks_values, player_card_open = save_df(env)
            turn_lst.append(turn)
            board_stocks_lst.append(board_stocks)
            player_name_lst.append(player_name)
            player_score_lst.append(player_score)
            player_stocks_values_lst.append(player_stocks_values)
            player_card_open_lst.append(player_card_open)
            # print('turn abla ', turn, board_stocks, player_name, player_score, player_stocks_values, player_card_open)

            if done == True:
                break
        df = pd.DataFrame({
            "turn": turn_lst,
            "board stocks": board_stocks_lst,
            "player name": player_name_lst,
            "player score": player_score_lst,
            "player stocks value": player_stocks_values_lst,
            "player card open": player_card_open_lst
        })
        df.to_csv('gym_splendor/DuDoan/Data/dat{}.csv'.format(ban))

if __name__ == '__main__':
    main()
