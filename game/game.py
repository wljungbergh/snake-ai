import pygame
import numpy as np
import random 



BG_COLOR_ = (18, 13, 49);
SNAKE_COLOR_ = (149, 198, 35)
HEAD_SNAKE_COLOR_ = (200, 240, 65)
FOOD_COLOR_ = (241, 218, 196)



class Simulator:
    def __init__(self, size = 20, max_steps = 200):
        self.size = size
        self.max_steps = max_steps

    def simulate(self):
        self.game = Game(self.size)

        while not self.game.game_over and self.game.moves_made < self.max_steps:
            self.game.change_dir(random.randint(0,3))
            self.game.next_move()
        

        return self.game.moves_made, self.game.snake.length


class Game:
    def __init__(self, size = 20):
        self.size = size
        self.snake = Snake([int(self.size/2), int(self.size/2)])
        self.moves_made = 0
        self.just_ate = False
        self.game_over = False
        self.game_won = False
        self.spawn_new_food()


    def reset(self):
        self.moves_made = 0
        self.game_over = False
        self.just_ate = False
        self.spawn_new_food()
        self.snake = Snake([int(self.size/2), int(self.size/2)])

    def change_dir(self, direction):
        self.snake.direction = direction
    
    def get_state(self):
        pos = self.snake.pos
        fp = self.food_pos
        state = [0]*12
        # collision states
        
        state[0] = (self.check_collision([a+b for a,b in zip(pos, [1,0])]))
        state[1] = (self.check_collision([a+b for a,b in zip(pos, [0,1])]))
        state[2] = (self.check_collision([a+b for a,b in zip(pos, [-1,0])]))
        state[3] = (self.check_collision([a+b for a,b in zip(pos, [0,-1])]))
        
        # food pos states
        if ((fp[0] > pos[0]) and (fp[1] == pos[1])): state[4]   = 1
        if ((fp[0] > pos[0]) and (fp[1] > pos[1])): state[5]    = 1
        if ((fp[0] == pos[0]) and (fp[1] > pos[1])): state[6]   = 1
        if ((fp[0] < pos[0]) and (fp[1] > pos[1])): state[7]    = 1
        if ((fp[0] < pos[0]) and (fp[1] == pos[1])): state[8]   = 1
        if ((fp[0] < pos[0]) and (fp[1] < pos[1])): state[9]    = 1
        if ((fp[0] == pos[0]) and (fp[1] < pos[1])): state[10]  = 1
        if ((fp[0] > pos[0]) and (fp[1] < pos[1])): state[11]   = 1
        return state

    def distance_to_food(self):
        dist = [abs(a - b) for a,b in zip(self.snake.pos, self.food_pos)]
        return dist[0] + dist[1]
    
    def create_obs(self, shape = (3,3,2)):
        grid = np.zeros(shape=shape, dtype=np.float32)
        #implement returning 3x3 occupancy grid
        raise NotImplementedError()

    def spawn_new_food(self):
        pos = np.random.randint(self.size, size=2)
        pos = pos.tolist()

        while pos in self.snake.body:
            pos = np.random.randint(self.size, size=2)
            pos = pos.tolist()

        self.food_pos = pos

    def next_move(self,):
        self.moves_made += 1
        self.snake.move()
        if self.snake.pos == self.food_pos:
            self.spawn_new_food()
            self.snake.length += 1
            if self.snake.length == self.size^2: self.game_won = True
            self.just_ate = True
            self.snake.body.pop()
            return

        if self.just_ate:
            self.just_ate = False
        else:
            self.snake.body.pop()

        if self.check_collision(self.snake.pos): 
            self.game_over = True

    def check_collision(self, pos):
        if pos in self.snake.body[1:]:
            return 1
        elif any(p > self.size-1 or p < 0 for p in self.snake.pos):
            return 1
        else:
            return 0
        




class GameBoard:
    def __init__(self, game, size = 20, show_score = False):
        self.game = game
        self.size = size
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
    
    def redraw(self):
        self.draw_bg()
        self.draw_food()
        self.draw_snake()
        if self.show_score:
            self.draw_score()


class Snake:
    def __init__(self, pos):
        self.pos = pos
        self.length = 1
        self.direction = 0
        self.body = [pos]

    def move(self):
        tmp = self.pos[:]

        if self.direction == 0:
            self.pos[0] += 1
        elif self.direction == 1:
            self.pos[1] += 1
        elif self.direction == 2:
            self.pos[0] += -1
        elif self.direction == 3:
            self.pos[1] += -1

        self.body.insert(1, tmp)
    
       

    
        
        

if __name__ == "__main__":
    size = 40
    gb = GameBoard(Game(size), size)
    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True
    running = False
    # The clock will be used to control how fast the screen updates

    # -------- Main Program Loop -----------
    while carryOn and not gb.game.game_over:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if not running:
                    running = True

                if event.key == pygame.K_LEFT:
                    #gb.next_move(2)
                    gb.game.change_dir(2)
                if event.key == pygame.K_UP:
                    #gb.next_move(3)
                    gb.game.change_dir(3)
                if event.key == pygame.K_RIGHT:
                    #gb.next_move(0)
                    gb.game.change_dir(0)
                if event.key == pygame.K_DOWN:
                    #gb.next_move(1)
                    gb.game.change_dir(1)

    



        # --- Go ahead and update the screen with what we've drawn.
        
        #gb.change_dir(random.randint(0, 3))
        if running:
            gb.game.next_move()
        gb.redraw()
        pygame.display.update()

        # --- Limit to 60 frames per second
        gb.clock.tick(15)

        #Once we have exited the main program loop we can stop the game engine:

    print("Your score was: {}".format(gb.game.snake.length))
    pygame.quit()


