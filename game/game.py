import pygame
import numpy as np
import random 



BG_COLOR = (18, 13, 49);
SNAKE_COLOR = (149, 198, 35)
HEAD_SNAKE_COLOR = (200, 240, 65)
FOOD_COLOR = (241, 218, 196)



class Game:
    def __init__(self, size = 20):
        self.size = size
        self.snake = Snake([int(self.size/2), int(self.size/2)])
        self.moves_made = 0
        self.just_ate = False
        self.game_over = False
        self.spawn_new_food()


    def change_dir(self, direction):
        self.snake.direction = direction
    
    def change_dir(self, direction):
        self.snake.direction = direction
            
    def spawn_new_food(self):
        pos = np.random.randint(self.size, size=2)
        pos = pos.tolist()

        while pos in self.snake.body:
            pos = np.random.randint(self.size, size=2)
            pos = pos.tolist()

        self.food_pos = pos

    def next_move(self,direction = 0):
        self.moves_made += 1
        #self.snake.direction = direction
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

        self.check_collision()


    
    def check_collision(self):
        if self.snake.pos in self.snake.body[1:]:
            self.game_over = True

        if any(p > self.size-1 or p < 0 for p in self.snake.pos):
            self.game_over = True



class GameBoard:
    def __init__(self, size = 20):
        self.game = Game(size)
        self.size = size
        self.width = 400
        self.height = 400
        self.boxsize = int(self.width/self.size)
        self.snake = Snake([int(self.size/2), int(self.size/2)])
        self.spawn_new_food()
        self.moves_made = 0
        self.game_over = False
        self.pygame_init()
        self.just_ate = False
        


    
    def pygame_init(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height),0,32)
        pygame.display.set_caption('snake-ai')
        self.screen.fill(BG_COLOR)
        self.clock = pygame.time.Clock()
        self.draw_snake()
        self.font = pygame.font.Font('freesansbold.ttf', 32) 

    def draw_food(self):
        top = self.game.food_pos[0] * self.boxsize
        left = self.game.food_pos[1] * self.boxsize
        pygame.draw.rect(self.screen,FOOD_COLOR, [top, left, self.boxsize, self.boxsize], 0)

    def draw_bg(self):
        self.screen.fill(BG_COLOR)

    def draw_score(self):
        font = pygame.font.SysFont(None, 16)
        img = font.render('score: {}'.format(self.snake.length), True, [255, 255, 255])
        self.screen.blit(img, (20, 20))
  
    def draw_snake(self):
        first = True
        #for pos in self.snake.body:
        for pos in self.game.snake.body:
            if first: 
                color = HEAD_SNAKE_COLOR
                first = False
            else:
                color = SNAKE_COLOR
            top = pos[0] * self.boxsize
            left = pos[1] * self.boxsize
           
            pygame.draw.rect(self.screen, color, [top, left, self.boxsize, self.boxsize],0)

    
    def redraw(self):
        self.draw_bg()
        self.draw_food()
        self.draw_snake()
        self.draw_score()


    def change_dir(self, direction):
        self.snake.direction = direction

    def spawn_new_food(self):
        pos = np.random.randint(self.size, size=2)
        pos = pos.tolist()

        while pos in self.snake.body:
            pos = np.random.randint(self.size, size=2)
            pos = pos.tolist()

        self.food_pos = pos
         
    

    def next_move(self,direction = 0):
        self.moves_made += 1
        #self.snake.direction = direction
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

        self.check_collision()


    
    def check_collision(self):
        if self.snake.pos in self.snake.body[1:]:
            self.game_over = True

        if any(p > self.size-1 or p < 0 for p in self.snake.pos):
            self.game_over = True

       

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
        
       

    
        
        


gb = GameBoard(20)
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates

# -------- Main Program Loop -----------
while carryOn and not gb.game_over:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            

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
    gb.next_move()
    gb.redraw()
    pygame.display.update()

    # --- Limit to 60 frames per second
    gb.clock.tick(15)

    #Once we have exited the main program loop we can stop the game engine:

print("Your score was: {}".format(gb.snake.length))
pygame.quit()


