import game.game as game
import gym
import pygame
import numpy as np
import matplotlib.pyplot as plt



BG_COLOR_ = (18, 13, 49);
SNAKE_COLOR_ = (149, 198, 35)
HEAD_SNAKE_COLOR_ = (200, 240, 65)
FOOD_COLOR_ = (241, 218, 196)



class SnakeEnv(game.GameBoard):
    def __init__(self, size=20):
        self.size = size
        self.game = game.Game(size)
        self.show_score = False
        self.width = 400
        self.height = 400
        self.boxsize = int(self.width/self.size)
        self.pygame_init()
    
    def pygame_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height),0,32)
        pygame.display.set_caption('snake-ai')
        self.screen.fill(BG_COLOR_)
        self.clock = pygame.time.Clock()
        self.draw_snake()
        if self.show_score:
            pygame.font.init()
            self.font = pygame.font.Font('freesansbold.ttf', 32) 

    def draw_food(self):
        top = self.game.food_pos[0] * self.boxsize
        left = self.game.food_pos[1] * self.boxsize
        pygame.draw.rect(self.screen,FOOD_COLOR_, [top, left, self.boxsize, self.boxsize], 0)

    def draw_bg(self):
        self.screen.fill(BG_COLOR_)

    def draw_score(self):
        font = pygame.font.SysFont(None, 16)
        img = font.render('score: {}'.format(self.game.snake.length), True, [255, 255, 255])
        self.screen.blit(img, (20, 20))
  
    def draw_snake(self):
        first = True
        for pos in self.game.snake.body:
            if first: 
                color = HEAD_SNAKE_COLOR_
                first = False
            else:
                color = SNAKE_COLOR_
            top = pos[0] * self.boxsize
            left = pos[1] * self.boxsize
           
            pygame.draw.rect(self.screen, color, [top, left, self.boxsize, self.boxsize],0)
    
    def render(self):
        self.draw_bg()
        self.draw_food()
        self.draw_snake()
        if self.show_score:
            self.draw_score()

    def step(self, action):
        self.game.change_dir(action)
        prev_dist = self.game.distance_to_food()
        self.game.next_move()
        new_dist = self.game.distance_to_food()

        obs = self.game.get_state()

        done = self.game.game_over or self.game.game_won

        reward = self.game.just_ate * 30 - 100*self.game.game_over - (prev_dist-new_dist)

        return np.array(obs), reward, done, {}
    
    

if __name__ == "__main__":
    
    se = SnakeEnv()
    done = False
    i = 0
    while not done:

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
        i += 1
        action = np.random.randint(0,4,1)
        obs, rew, done, info = se.step(action)
        se.render()
        pygame.display.update()
        se.clock.tick(10)



    pygame.quit()


    
        
