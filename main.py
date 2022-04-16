import gym
import gym_splendor
import os
import pandas as pd
def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <10:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break

if __name__ == '__main__':
    main()


def create_train(link_folder):
    list_stock = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
    file_train = pd.DataFrame({})
    for type_stock in list_stock[:-1]:
        for i in range(8):
            list_score = [100]*90
            file_train[f'{i}_{type_stock}_board'] = list_score
        for i in range(8):
            list_score = [100]*90
            file_train[f'{i}_{type_stock}_player'] = list_score
        for i in range(19):
            list_score = [100]*90
            file_train[f'{i}_{type_stock}_const'] = list_score
    for i in range(6):
        list_score = [100]*90
        file_train[f'{i}_auto_color_board'] = list_score
        file_train[f'{i}_auto_color_player'] = list_score
    file_train.to_csv(f'{link_folder}/file_train.csv', index=False)
    print(file_train.shape)

link_folder = './TRAIN_HIEU'
create_train(link_folder)





















