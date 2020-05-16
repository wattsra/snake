import pygame
import random
import os

snake_size = scale_factor = 4
scale_x = 20
scale_y = 20
max_x = scale_x * scale_factor
max_y = scale_y * scale_factor
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
loc = []
startingspeed = 10
class Snake():
    def __init__(self):
        global loc
        start_x = int(max_x//2)#xposition
        start_y = int(max_y//2)#y position
        self.dir_x=0
        self.dir_y=1
        loc = [(start_x,start_y),]

#### NEED TO SWAP X AND Y DIRECTIONS

    def move(self):
        global loc, f, s, run,game
        n = len(loc)
        new_locs = [0]*n
        for i in range(n-1):
            new_locs[i+1] = loc[i]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # or event.type == pygame.KEYUP
                if event.key == pygame.K_q:
                    game = False
            # else:
            #     if event.key == pygame.K_q:
            #         run = True
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
        #for i in range(len(loc)):
        x,y = loc[0][0], loc[0][1]
        if (x < 0):
            #and self.dir_x ==-1: #
            new_locs[0] = ((max_x-snake_size), (y))
        elif (y < 0):
            #and self.dir_y ==-1: #
            new_locs[0] = (x, (max_y-snake_size))
        elif (x >= (max_x-snake_size))and self.dir_x ==1: #
            new_locs[0] = ((0), (y))
        elif (y > (max_y-snake_size)):
            #and self.dir_y ==1: #
            new_locs[0] = (x, (0))
        else:
            new_locs[0] = ((loc[0][0] + self.dir_x*snake_size),(loc[0][1] + self.dir_y*snake_size))
        ### check for eating fruits ###
        for fruit in f.fruits:
            if (fruit[0]-snake_size < loc[0][0] < (fruit[0]+snake_size)) and fruit[1]-snake_size < loc[0][1] < (fruit[1]+snake_size):
                new_locs.append(loc[-1])
                f.eat(fruit)
        ### check for crashing###
        for i in range(len(new_locs)-1):
            if new_locs[i+1][0] == new_locs[0][0] and new_locs[i+1][1] == new_locs[0][1]:
                game = False
        loc = new_locs

    def draw(self,screen):
        for i in range(len(loc)):
            pygame.draw.rect(screen, WHITE, (loc[i][0], loc[i][1], snake_size, snake_size))
            if i == 0:
                pygame.draw.rect(screen, RED,(loc[i][0]+(snake_size/4), loc[i][1]+(snake_size/4), snake_size/4, snake_size/4))
    def eat(self):
        loc.append((loc[-1][0],loc[-1][1]))

def drawText(screen,text,size,font,color,bgcolor=None,center=False,padding=None):
    if padding:
        print("padding for ",text)
        padx=padding[0]
        pady = padding[1]
    else:
        padx,pady = 0,int(size)
    font = pygame.font.Font(font, size)
    text = font.render(text,True,color,bgcolor)
    textRect = text.get_rect()
    if center:
        if center in ["x","xy","yx"]:
            textRect.centerx = screen.get_rect().centerx + padx
            textRect.centery = pady
        if center in ["y","xy","yx"]:
            textRect.centery = screen.get_rect().centerx + pady
            textRect.centerx = padx

    screen.blit(text,textRect)



def drawWindow(screen):
    global s, win,score,level
    screen.fill(BLACK)
    s.draw(screen)
    f.draw(screen)
    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    drawText(win,"Score: "+ str(score),28,'Roboto-Bold.ttf',WHITE,center="x")
    drawText(win,"level: "+ str(level),12,'Roboto-Bold.ttf',WHITE,bgcolor=RED)

    pygame.display.update()

def drawLoseWindow(screen):
    global s, win,score,high
    font = pygame.font.Font('Roboto-Bold.ttf', 32)
    text = font.render('YOU LOSE', True, WHITE, RED)
    textRect = text.get_rect()
    textRect.center = win.get_rect().center
    win.blit(text, textRect)
    font2 = pygame.font.Font('Roboto-Bold.ttf', 20)
    text2 = font2.render('Score: '+ str(score), True, WHITE,BLACK)
    text2Rect = text2.get_rect()
    text2Rect.center = win.get_rect().center
    text2Rect.centery = text2Rect.centery + 50
    win.blit(text2, text2Rect)
    text3 = font2.render('High Score: '+ str(high), True, WHITE,BLACK)
    text3Rect = text3.get_rect()
    text3Rect.center = win.get_rect().center
    text3Rect.centery = text3Rect.centery + 70
    win.blit(text3, text3Rect)
    pygame.display.update()

class Fruits():
    def __init__(self):
        self.fruits = []

        #self.fruits = [(6*scale_factor,6*scale_factor)]
    def add_random(self):
        global loc
        check = True
        while check:
            new_fruit = (random.randint(1,scale_x-1)*scale_factor,random.randint(1,scale_y-1)*scale_factor)
            if new_fruit not in loc[1:]:
                self.fruits.append(new_fruit)
                check = False
    def draw(self,screen):
        for i in range(len(self.fruits)):
            pygame.draw.rect(screen, RED, (self.fruits[i][0], self.fruits[i][1], snake_size, snake_size))
    def eat(self,fruit):
        global score
        self.fruits.pop(self.fruits.index(fruit))
        score += 100
        self.add_random()

def speedupdate():
    global score
    level = (score // 400) +1
    speed = int(level + startingspeed)
    return speed, level

def startmenu(screen):
    global win, game, score,run
    screen.fill(BLACK)
    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    drawText(win,"Welcome to Snake",28,'Roboto-Bold.ttf',WHITE,center="x")
    drawText(win, "Press any key to start game!", 14, 'Roboto-Bold.ttf', WHITE,
             center="x",padding=(0,80))
    pygame.display.update()
    start = True
    while start == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # or event.type == pygame.KEYUP
                if event.key == pygame.K_q:
                    run = False
                else:
                    game = True
                    score = 0
                    start = False

def main():
    global s, win, f, run, score,high, level, game, start
    run = True
    start = True
    while run:
        win = pygame.display.set_mode((max_x*scale_factor,max_y*scale_factor)) # pixel scaling *6 on display
        screen = pygame.Surface((max_x,max_y)) # put screen on window to allow for scaling
        pygame.init()
        startmenu(screen)
        s = Snake()
        f = Fruits()
        f.add_random()
        while game:
            clock = pygame.time.Clock()
            score += 1
            speed, level = speedupdate()
            pygame.time.delay(5)
            clock.tick(speed)
            drawWindow(screen)
            s.move()

        if os.path.exists("HighScore.txt"):
            with open("HighScore.txt","r") as f:
                high = int(f.read())
                if score > high:
                    high = score
                    f = open("HighScore.txt","w")
                    f.write(str(high))
                    f.close()
        else:
            high = score
            f = open("HighScore.txt", "w")
            f.write(str(high))
            f.close()
        drawLoseWindow(screen)
        pygame.time.delay(4000)

main()
