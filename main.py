import gym
import gym_splendor
import pandas as pd


def save_df(env, player_ids_target):
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
    player_card_close = []
    turn.append(obj["Turn"])
    board_stocks.append(board.stocks)
    board_hien_the.append(board.hien_the())
    t = 0
    for p in player:
        # print(p.name, p.score, list(p.stocks.values()), end="")
        player_name.append(p.name)
        player_score.append(p.score)
        player_stocks_values.append(p.stocks.values())
        # print(" Card got: ", end="")
        player_card_open[p.name] = []
        for i in p.card_open:
            player_card_open[p.name].append(i.id)

    target_player = player_name[player_ids_target]
    # print('target player ', target_player)
    for p in player:
        if p.name == target_player:
            for i in p.card_upside_down:
                player_card_close.append(i.id)

    # target_player = player_name[player_ids_target]
    # player_card_close.append(player[target_player].card_upside_down)
    return turn, board_stocks, player_name, player_score, player_stocks_values, player_card_open, player_card_close


def main():
    # env = gym.make('gym_splendor-v0')
    # env.reset()
    env = gym.make('gym_splendor-v0')
    for ban in range(1000):
        if ban % 100 == 0:
            print('processing ', ban/1000 * 100)
        env.reset()
        turn_lst = []
        board_stocks_lst = []
        player_name_lst = []
        player_score_lst = []
        player_stocks_values_lst = []
        player_card_open_lst = []
        player_card_close_lst = []

        while env.turn < 200:
            o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
            # env.render()
            turn, board_stocks, player_name, player_score, \
            player_stocks_values, player_card_open, player_card_close = save_df(env, 1)
            turn_lst.append(turn)
            board_stocks_lst.append(board_stocks)
            player_name_lst.append(player_name)
            player_score_lst.append(player_score)
            player_stocks_values_lst.append(player_stocks_values)
            player_card_open_lst.append(player_card_open)
            player_card_close_lst.append(player_card_close)
            # print('turn abla ', turn, board_stocks, player_name, player_score, player_stocks_values, player_card_open)

            if done == True:
                break
        df = pd.DataFrame({
            "turn": turn_lst,
            "board stocks": board_stocks_lst,
            "player name": player_name_lst,
            "player score": player_score_lst,
            "player stocks value": player_stocks_values_lst,
            "player card open": player_card_open_lst,
            "player target card close": player_card_close_lst
        })
        df.to_csv('gym_splendor/DuDoan/Raw_data/dat{}.csv'.format(ban))

if __name__ == '__main__':
    main()
