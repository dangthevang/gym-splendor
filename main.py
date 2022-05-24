
import gym
import gym_splendor
import pandas as pd
import time
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
def main():
    env = gym.make('gym_splendor-v0')
    env.reset() 
    start_time = time.time()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break
    for i in range(4):
        # print(env.turn//4)
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
    # print(env.pVictory)
    print(time.time()-start_time)

# main()
def run1():
    with suppress_stdout():
        name = main()
    print(name)


import multiprocessing
if __name__ != "main":
    start_time = time.perf_counter()
 
    # Creates two processes
    p1 = multiprocessing.Process(target=run1)
    p2 = multiprocessing.Process(target=run1)
    p3 = multiprocessing.Process(target=run1)
    p4 = multiprocessing.Process(target=run1)
    p5 = multiprocessing.Process(target=run1)
    p6 = multiprocessing.Process(target=run1)
 
    # Starts both processes
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
 
    finish_time = time.perf_counter()
 
    print(f"Program finished in {finish_time-start_time} seconds")