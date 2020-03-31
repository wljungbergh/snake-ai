import game.game as game
import pygame
import numpy as np
import pickle

BG_COLOR_ = (18, 13, 49);
SNAKE_COLOR_ = (149, 198, 35)
HEAD_SNAKE_COLOR_ = (200, 240, 65)
FOOD_COLOR_ = (241, 218, 196)



class SnakeEnv():
    def __init__(self, size=20, rendering = True):
        self.size = size
        self.obs_size = [2,2,2,2,9]
        self.act_size = 4
        self.game = game.Game(size)
        self.show_score = False
        self.width = 400
        self.height = 400
        self.boxsize = int(self.width/self.size)
        if rendering:
            pygame.init()
    
    def pygame_init(self):
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
        #self.draw_obs()
        if self.show_score:
            self.draw_score()

    def draw_obs(self):
        (tmp1, tmp2, tmp3, tmp4, _) = self.game.get_state()
        top = self.game.snake.pos[0] 
        left = self.game.snake.pos[1]
        color_free = (255,255,255)
        color_occ = (128,0,0)
        
        if tmp1:
            pygame.draw.rect(self.screen, color_occ,    [(top+1)*self.boxsize, (left+0)*self.boxsize, self.boxsize, self.boxsize],0)
        else:
            pygame.draw.rect(self.screen, color_free,   [(top+1)*self.boxsize, (left+0)*self.boxsize, self.boxsize, self.boxsize],0)
        if tmp2:
            pygame.draw.rect(self.screen, color_occ,    [(top+0)*self.boxsize, (left+1)*self.boxsize, self.boxsize, self.boxsize],0)
        else:
            pygame.draw.rect(self.screen, color_free,   [(top+0)*self.boxsize, (left+1)*self.boxsize, self.boxsize, self.boxsize],0)
        if tmp3:
            pygame.draw.rect(self.screen, color_occ,    [(top-1)*self.boxsize, (left+0)*self.boxsize, self.boxsize, self.boxsize],0)
        else:
            pygame.draw.rect(self.screen, color_free,   [(top-1)*self.boxsize, (left+0)*self.boxsize, self.boxsize, self.boxsize],0)
        if tmp4:
            pygame.draw.rect(self.screen, color_occ,    [(top+0)*self.boxsize, (left-1)*self.boxsize, self.boxsize, self.boxsize],0)
        else:
            pygame.draw.rect(self.screen, color_free,   [(top-0)*self.boxsize, (left-1)*self.boxsize, self.boxsize, self.boxsize],0)

        pass

    def reset(self):
        self.game.reset(self.size)
        self.boxsize = int(self.width/self.size)

    def transform_action(self, action):
        shifted_action = action - 1
        direction = (self.game.snake.direction + shifted_action) % 4
        return direction 

    def step(self, action):
        self.game.change_dir(action)
        prev_dist = self.game.distance_to_food()
        self.game.next_move()
        new_dist = self.game.distance_to_food()

        state = self.game.get_state()

        done = self.game.game_over or self.game.game_won

        if self.game.game_over: 
            info = "game over"

        elif self.game.game_won:
            info = "game won"
            print("game won")
        else:
            info = ""

        reward = self.game.just_ate * 300 - 1000*self.game.game_over + (prev_dist-new_dist)
        #if done:
            #reward += (self.game.snake.length-1) * 50
        
        #reward = self.game.just_ate * 1 - 100*self.game.game_over - 0.01
        #reward = 0 - 100*done + 30 
        return state, reward, done, info