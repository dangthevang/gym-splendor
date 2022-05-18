
import gym
import gym_splendor
import pandas as pd
import time

def main():
    env = gym.make('gym_splendor-v0')
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_1.csv', index = False)
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_2.csv', index = False)
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_3.csv', index = False)
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_4.csv', index = False)
    try:
        state_save = pd.read_csv('state.csv')
    except:
        pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []})


    env.reset()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
        env.render()
        if done == True:
            break
    state = env.state
    print(check_winner(state))
    for player in list(state['Player']):
        df_tam = pd.read_csv(f'State_tam_{player.name}.csv')
        state_save = pd.concat([state_save, df_tam])
    if check_winner(state) != "NA0":
        df_tam = pd.read_csv(f'State_tam_{player.name}.csv')
        state_save.to_csv('state.csv', index = False)
    for i in range(4):
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
if __name__ == '__main__':
    main()


