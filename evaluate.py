import pickle
import numpy as np
from env import environment as env
np.random.seed(1337)

NUMBER_OF_EVALUATIONS = 1000
SIZE = 40
with open("qtables/qtable1.pickle", 'rb') as f:
    qtable = pickle.load(f)


if __name__ == '__main__':
    se = env.SnakeEnv(SIZE, rendering=False)
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

        total_length += se.game.snake.length
        se.reset()

    print("Average length of snake was: {} ".format(total_length/NUMBER_OF_EVALUATIONS))
    print("Max length of snake was: {} ".format(max_len))
    print("Number of evaluations was: {} ".format(NUMBER_OF_EVALUATIONS))