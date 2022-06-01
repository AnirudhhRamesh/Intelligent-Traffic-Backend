from fileinput import filename
from random import randint
from turtle import Screen, color, width
import pygame
from pygame.locals import *
import sys
from cell import Cell
from car import Car
from map import Map

from passenger import Passenger
 
 
# pygame.draw.polygon(surface, color, pointlist, width)
# pygame.draw.line(surface, color, start_point, end_point, width)
# pygame.draw.lines(surface, color, closed, pointlist, width)
# pygame.draw.circle(surface, color, center_point, radius, width)
# pygame.draw.ellipse(surface, color, bounding_rectangle, width)
# pygame.draw.rect(surface, color, rectangle_tuple, width)

    # Setting up color objects
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAX_X = 600
MAX_Y = 600
FPS = 30

# Assign FPS a value
FramePerSec = pygame.time.Clock()
margin = 1

# DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))

#GUI description
class GUI:

    def __init__(self, map) -> None:
        self.map = map
        self.grid = []
        for row in range(len(map.map)):
            self.grid.append([])
            for column in range(len(map.map[0])):
                self.grid[row].append(0)  
        self.cell_width = self.cell_height = MAX_X/(len(self.map.map)+1)


    def launchGUI(self):
        pygame.init()


        # window size
        DISPLAYSURF.fill(BLACK)
        pygame.draw.line(DISPLAYSURF, BLACK, (0, 0), (MAX_X, 0))
        pygame.draw.line(DISPLAYSURF, BLACK, (0, 0), (0, MAX_Y))
        pygame.draw.line(DISPLAYSURF, BLACK, (MAX_X, 0), (MAX_X, MAX_Y))
        pygame.draw.line(DISPLAYSURF, BLACK, (0, MAX_Y), (MAX_X, MAX_Y))

    def update(self):

        #create array to select map cell
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = int(pos[0] // (self.cell_width+margin))
                row = int(pos[1] // (self.cell_height+margin))
                if self.map.map[column][row].isRoad and not self.map.map[column][row].hasPassenger(): 
                    self.grid[column][row] = 1
                    finalCell = self.map.getCell(randint(0, len(self.map.map)-1), randint(0,len(self.map.map[0])-1))
                    while not finalCell.isRoad :
                        finalCell = self.map.getCell(randint(0, len(self.map.map)-1), randint(0,len(self.map.map[0])-1)) 
                    newPassenger = Passenger(self.map.getCell(column, row), finalCell)
                    self.map.add_passenger(newPassenger)
                    self.map.map[column][row].passenger = newPassenger

        #Draw the grid
        for row in range(len(self.grid[0])):
            for column in range(len(self.grid)):
                if self.map.map[column][row].isRoad and not self.map.map[column][row].hasPassenger():
                    color = WHITE
                else:
                    color = BLACK
                if self.grid[column][row] == 1:
                    color = GREEN
                pygame.draw.rect(DISPLAYSURF, 
                                 color, 
                                 [(margin+self.cell_width)*column+margin,
                                 (margin+self.cell_height)*row+margin, self.cell_width, self.cell_height])  
        FramePerSec.tick(FPS)
        pygame.display.flip()