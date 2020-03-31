import pickle
import numpy as np
from env.environment import *
import pygame 

np.random.seed(1337)

NUMBER_OF_EVALUATIONS = 1000
SIZE = 40
with open("qtables/qtable.pickle", 'rb') as f:
    qtable = pickle.load(f)


if __name__ == '__main__':
    se = SnakeEnv(size=SIZE)
    se.pygame_init()
    total_length = 0
    max_len = 0


    for i in range(NUMBER_OF_EVALUATIONS):
        state = se.game.get_state()
        done = False
            

        while not done: 
            
            
            
            action_list = np.argsort(qtable[state])
            action = action_list[-1]
            if not se.game.valid_move(action):
                action = action_list[-2]
            state, rew, done, info = se.step(action)
            


        if se.game.snake.length > max_len:
            max_len = se.game.snake.length
            ep = i

        total_length += se.game.snake.length
        se.reset()

    print("Average length of snake was: {} ".format(total_length/NUMBER_OF_EVALUATIONS))
    print("Max length of snake was: {} @ espisode {} ".format(max_len, ep))
    print("Number of evaluations was: {} ".format(NUMBER_OF_EVALUATIONS))