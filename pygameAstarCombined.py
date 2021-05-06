import math
import sys
import random
import time
import pygame
import tkinter as tk

obstacles = []
short_path = []
explored = []

class Node():
    """Start Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
        self.u = 0

    def __eq__(self, other):
        return self.position == other.position

def Obstacle(baby_position):
    """Avoid obstacles while finding children"""
    corner = 0
    corner1_position = (baby_position[0] - 1, baby_position[1])
    corner2_position = (baby_position[0] , baby_position[1] - 1)
    for obstacle in obstacles:
        if baby_position == obstacle.pos:
            return 1
        if (corner1_position == obstacle.pos) or (corner2_position == obstacle.pos):
            corner +=1
    if corner > 1:
        return 1
        
    return 0

def ACTIONS(matrix, start, end, c):
    """Returns a list of points as a path from the start to the end"""

    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    start_node.u = 0
    end_node = Node(None, end)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0
    end_node.u = 0

    
    open_list = []
    closed_list = []
    vertices = []
    vertex_list = []

    open_list.append(start_node)
   

    #loop through list
    while len(open_list) > 0:
    
        
        current_node = open_list[0]
        current_index = 0
        for index, inode in enumerate(open_list):
            if inode.u > current_node.u:
                current_node = inode
                current_index = index

        
        open_list.pop(current_index)
        closed_list.append(current_node)
           

        if current_node == end_node:
            goal = []
            current = current_node
            while current is not None:
                goal.append(current.position)
                current = current.parent
                
            return goal[::-1]
            

        #make babies
        children = []
        
        for new_frontier in [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]: 
         
            #check neighbors
            baby_position = (current_node.position[0] + new_frontier[0], current_node.position[1] + new_frontier[1])

            explored.append(baby_position)
            
            
            if baby_position[0] > 100 or baby_position[0] < 0 or baby_position[1] > 100 or baby_position[1] < 0:
                continue

                        
            x = Obstacle(baby_position)

            if x == 1:
                continue

            
            baby_node = Node(current_node, baby_position)

            
            children.append(baby_node)

        
        
        for child in children:
           
            
            for closed_child in closed_list:
                if child == closed_child:
                    continue

        
            child.g = current_node.g + 1
            child.h = math.sqrt((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            if child.h == 0:
                child.h = 1
            child.f = child.g + child.h
            if child.f >= c:
                continue 
            child.u = (c - child.g) / child.h
                       
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
             
            open_list.append(child)

    print('Path does not exist')
 
class cube(object):
    """Basic building blocks for the robot and obstacles"""
    rows = 100
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
       
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
 
 
class robot(object):
    """The little red guy who does the exploring"""
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
 
    def move(self, path):
    
            self.dirnx = path[0] - self.head.pos[0]
            self.dirny = path[1] - self.head.pos[1]
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            for i, c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0],turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                    else: c.move(c.dirnx,c.dirny)
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (0,0,0), (x,0),(x,w))
        pygame.draw.line(surface, (0,0,0), (0,y),(w,y))
       
 
def redrawWindow(surface):
    """Updates movement in real time"""
    global rows, width, s, finish, exp
    surface.fill((0,0,0))
    s.draw(surface)
    for obstacle in obstacles:
        obstacle.draw(surface)
    drawGrid(width,rows, surface)
    finish.draw(surface)
    exp.draw(surface)
    pygame.display.update()
 
 
def randomObstacle(rows, item):
    """Creates the obstacles"""
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)

def ARastar(win, start, end, c):
    """Continually finds the best path"""
    global exp
    short_path = ACTIONS(win, start, end, c)
    flag = False
    if short_path:
        flag = True
    while flag:
        for e in explored:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    obstacle = cube(pos, color=(0,255,0))
                    obstacle.draw(win)
                    obstacles.append(obstacle)
                    ARastar(win, start, end, c)
                    redrawWindow(win)
            pygame.time.delay(100)
            clock.tick(10)
            s.move(e)
            exp = cube(e, color=(0,0,255))
                
            redrawWindow(win)
  
def main():
    global width, rows, s, finish, clock, exp
    width = 500
    rows = 100
    win = pygame.display.set_mode((width, width))
    s = robot((255,0,0), (0,0))
    x = 1
    start = (0, 0)
    end = (55, 72)
    finish = cube(end, color=(255,0,0))
    c = 1000000
    while x < 1000:
        x += 1
        obstacle = cube(randomObstacle(rows, s), color=(0,255,0))
        obstacles.append(obstacle)
    clock = pygame.time.Clock()
    redrawWindow(win)
    ARastar(win, start, end, c)
main()

