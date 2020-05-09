from time import perf_counter
from typing import List, Any
import pygame


dificulty = 4
max_x = 100
max_y = 100
scale_factor = 4
snake_size = 5
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
loc = []
#fruits = []

# class GameManager():
#     def __init__(self):
#         self.timer = None
#         global loc
#         pass
#
#     def start_timer(self):
#         self.timer = perf_counter()
#         #print(self.timer)
#         return self.timer
#
#     def current_tick(self):
#         tick = perf_counter() - self.timer
#         return tick
#
#     def stop_timer(self):
#         if self.timer is None:
#             raise TimerError("Timer not running")
#         self.timer = None
#
#     def tick(self):
#         global loc
#         while self.timer:
#             if self.current_tick() >= 0.1:
#                 #print("tick")
#                 self.stop_timer()
#                 self.start_timer()
#                 self.update_score()
#                 self.snake.controls()
#                 self.snake.move()  # need to create snake class with move function
#
#     def update_score(self):
#         print("snakehead",self.snake.head())
#         if self.snake.head in self.fruits:
#             self.score +=1
#         pass
#
#     def start(self):
#         self.start_timer()
#         self.snake = Snake()
#         self.fruits = Fruits().fruits

class Snake():
    def __init__(self):
        global loc
        start_x = max_x//2#xposition
        start_y = max_y//2#y position
        v = 0.1 * (dificulty ** 2) #velocity multiplied by the square of the difficult number
        self.dir_x=1
        self.dir_y=0
        start_length = 2
        loc = [(start_x,start_y),]

#### NEED TO SWAP X AND Y DIRECTIONS

    def move(self):
        global loc
        for event in pygame.event.get():
            #print(event)
            #if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if self.dir_y != -1:
                    self.dir_y = 1
                    self.dir_x = 0
            elif keys[pygame.K_UP]:
                if self.dir_y != 1:
                    self.dir_y = -1
                    self.dir_x = 0
            elif keys[pygame.K_LEFT]:
                if self.dir_x != 1:
                    self.dir_y = 0
                    self.dir_x = -1
            elif keys[pygame.K_RIGHT]:
                if self.dir_x != -1:
                    self.dir_y = 0
                    self.dir_x = 1
        for i in range(len(loc)):
            x,y = loc[i][0], loc[i][1]
            if (x <= 0 and self.dir_x ==-1):
                loc[i] = ((max_x-1), (y))
            elif (y <= 0 and self.dir_y ==-1):
                loc[i] = (x, (max_y-1))
            elif (x >= (max_x-snake_size) and self.dir_x ==1):
                loc[i] = ((0), (y))
            elif (y >= (max_y-snake_size) and self.dir_y ==1):
                loc[i] = (x, (0))
            else:
                loc[i] = ((loc[i][0] + self.dir_x),(loc[i][1] + self.dir_y))

    def draw(self,screen):
        pygame.draw.rect(screen, WHITE, (loc[0][0], loc[0][1], snake_size, snake_size))

    def eat(self):
        pass

    def collision(self):
        pass

    def head(self):
        return loc[0]

    def controls(self):
        pass

def drawWindow(screen):
    global s, win
    screen.fill(BLACK)
    s.draw(screen)
    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    pygame.display.update()


class Fruits():
    def __init__(self):
        self.fruits = [(3,6)]
    def add_random(self):
        self.fruits.append((4,5))
        pass

def main():
    global s, win
    #pygame.init()
    win = pygame.display.set_mode((max_x*scale_factor,max_y*scale_factor)) # pixel scaling *6 on display
    screen = pygame.Surface((max_x,max_y)) # put screen on window to allow for scaling
    #game = GameManager()
    #game.start()
    s = Snake()
    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.time.delay(20)
        clock.tick(20)
        drawWindow(screen)
        s.move()

main()
