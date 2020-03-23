import game.game as game
import gym
from gym import spaces


class SnakeEnv(gym.Env):
    def __init__(self):
        super(SnakeEnv).__init__()
        self.game = game.Game(20)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low = 0, high=1, shape=(3,3,2))

    def step(self, action):
        self.game.change_dir(action)
        self.game.next_move()


        done = self.game.game_over
        reward = self.game.snake.length
        

    def reset(self):
        pass

    def render(self, mode = 'human', close = False):
        pass




g = game.Game(20)



