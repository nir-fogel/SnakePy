import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
DARK_GREEN = (1,50,32) 
LIGHT_GREEN = (0,200,0)


class Cube(object):
    rows = 20
    width = 500
    def __init__(self, start, dirnx=1, dirny=0, color=BLUE):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def Move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + dirnx, self.pos[1] + dirny)
    
    def Draw(self, surface, eyes=False):
        distance = self.width // self.rows
        row = self.pos[0]
        col = self.pos[1]

        pygame.draw.rect(surface, self.color, (row*distance+1, col*distance+1, distance-2, distance-2))
        if eyes:
            centre = distance//2
            radius = 3
            left_eye_middle = (row*distance+centre-radius,col*distance+8)
            right_eye_middle = (row*distance + distance -radius*2, col*distance+8)
            
            pygame.draw.circle(surface, WHITE, left_eye_middle, radius)
            pygame.draw.circle(surface, WHITE, right_eye_middle, radius)
            
            pygame.draw.circle(surface, BLACK, left_eye_middle, 1)
            pygame.draw.circle(surface, BLACK, right_eye_middle, 1)





class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def Move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 
                    
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 
        for index, cube in enumerate(self.body):
            p = cube.pos[:]
            if p in self.turns: # Check cube direction of movement
                turn = self.turns[p]
                cube.Move(turn[0], turn[1])
                if index == len(self.body)-1:
                    self.turns.pop(p)
            else:  # Check borders
                if cube.dirnx == -1 and cube.pos[0] <= 0: 
                    cube.pos = (cube.rows-1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows-1: 
                    cube.pos = (0,cube.pos[1])
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows-1: 
                    cube.pos = (cube.pos[0], 0)
                elif cube.dirny == -1 and cube.pos[1] <= 0: 
                    cube.pos = (cube.pos[0],cube.rows-1)
                
                else: 
                    cube.Move(cube.dirnx,cube.dirny)



    def Reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def AddCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def Draw(self, surface):
        for index, cube in enumerate(self.body):
            if index == 0:
                cube.Draw(surface, eyes=True)
            else:
                cube.Draw(surface)


def DrawGrid(width, rows, surface):
    sizeBetween = width // rows

    x = 0
    y = 0
    for l in range(rows):
        x += sizeBetween
        y += sizeBetween

        pygame.draw.line(surface, LIGHT_GREEN,(x,0), (x,width))
        pygame.draw.line(surface, LIGHT_GREEN,(0,y), (width,y))


def ReDrawWindow(surface):
    global rows, width, snake, apple
    surface.fill(DARK_GREEN)
    apple.Draw(surface)
    snake.Draw(surface)
    DrawGrid(width, rows, surface)
    pygame.display.update()


def RandomAppleCords(rows, snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda x:x.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def Message(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, snake, apple
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake(BLUE, (10,10))
    apple = Cube(RandomAppleCords(rows, snake), color=RED)
    clock = pygame.time.Clock()
    
    flag = True
    while flag:
        #pygame.time.delay(50)
        clock.tick(10)
        snake.Move()
        if snake.body[0].pos == apple.pos:
            snake.AddCube()
            apple = Cube(RandomAppleCords(rows, snake), color=RED)
        
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z:z.pos,snake.body[x+1:])):
                Message('You Lost:(',"Score: " + str(len(snake.body)) + '\nPlay again...')
                snake.Reset((10,10))
                break
        
        ReDrawWindow(win)
    
main()


