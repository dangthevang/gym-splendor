
import gym
import gym_splendor
import pandas as pd
import time

def main(env):
    # env = gym.make('gym_splendor-v0')
    env.reset() 
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        # env.render()
        if done == True:
            break
    for i in range(4):
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
    dict_result = {}
    for p in env.player:
        dict_result[p.name] = p.score
    sort_list = sorted(dict_result.items(), key=lambda x:x[1], reverse= True)
    sort_player = [item[0] for item in sort_list]
    sort_score = [item[1] for item in sort_list]
    return sort_player, sort_score


if __name__ == '__main__':
    env = gym.make('gym_splendor-v0')
    try:
        result_for_elo = pd.read_csv('data_for_elo.csv')
    except:
        result_for_elo = pd.DataFrame({'player':[], 'score':[]})
    list_player = []
    list_score = []
   

    for i in range(1, len(env.list_all_game)+1):
    # for i in range(1, 10):
        print('Game', i)
        x, y = main(env)
        list_player.append(x)
        list_score.append(y)
        env.id_tran += 1
    list_player = list(result_for_elo['player']) + list_player
    list_score = list(result_for_elo['score']) + list_score
    result_for_elo_new = pd.DataFrame()
    result_for_elo_new['player'] = list_player
    result_for_elo_new['score'] = list_score
    result_for_elo_new.to_csv('data_for_elo.csv', index= False)


    # print(env.list_all_game[:10])