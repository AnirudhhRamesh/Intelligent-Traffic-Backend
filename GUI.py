from random import randint
from turtle import Screen, color, width
import pygame
from pygame.locals import *
import sys
from cell import Cell

from passenger import Passenger
 
 
# pygame.draw.polygon(surface, color, pointlist, width)
# pygame.draw.line(surface, color, start_point, end_point, width)
# pygame.draw.lines(surface, color, closed, pointlist, width)
# pygame.draw.circle(surface, color, center_point, radius, width)
# pygame.draw.ellipse(surface, color, bounding_rectangle, width)
# pygame.draw.rect(surface, color, rectangle_tuple, width)


#GUI description
class GUI:
    def __init__(self, map) -> None:
        self.map = map
        self.grid = []
        for row in range(len(map.map)):
            self.grid.append([])
            for column in range(len(map.map[0])):
                self.grid[row].append(0)  

    def update(self):
        pygame.init()
        # Assign FPS a value
        FPS = 30
        FramePerSec = pygame.time.Clock()
    
        # Setting up color objects
        BLUE  = (0, 0, 255)
        RED   = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
    
        MAX_X = 600
        MAX_Y = 600

        cell_width = cell_height = MAX_X/(len(self.map.map)+1)
        margin = 1

        # window size
        DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
        DISPLAYSURF.fill(BLACK)
    
        pygame.draw.line(DISPLAYSURF, BLACK, (0, 0), (MAX_X, 0))
        pygame.draw.line(DISPLAYSURF, BLACK, (0, 0), (0, MAX_Y))
        pygame.draw.line(DISPLAYSURF, BLACK, (MAX_X, 0), (MAX_X, MAX_Y))
        pygame.draw.line(DISPLAYSURF, BLACK, (0, MAX_Y), (MAX_X, MAX_Y))

        #draw grid

        #create array to select map cell
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = int(pos[0] // (cell_width+margin))
                row = int(pos[1] // (cell_height+margin))
                if self.map.map[column][row].isRoad and not self.map.map[column][row].hasPassenger: 
                    self.grid[column][row] = 1
                    finalCell = self.map.getCell(randint(0, len(self.map.map)-1), randint(0,len(self.map.map[0])-1))
                    while not finalCell.isRoad :
                        finalCell = self.map.getCell(randint(0, len(self.map.map)-1), randint(0,len(self.map.map[0])-1)) 
                    self.map.add_passenger(Passenger(self.map.getCell(column, row), finalCell))
                    self.map.map[column][row].hasPassenger = True
                        
        #Draw the grid
        for row in range(len(self.grid[0])):
            for column in range(len(self.grid)):
                color = BLACK
                if self.map.map[column][row].isRoad and not self.map.map[column][row].hasPassenger:
                    color = WHITE
                # else:
                #     color = BLACK
                if self.grid[column][row] == 1:
                    color = GREEN
                pygame.draw.rect(DISPLAYSURF, 
                                 color, 
                                 [(margin+cell_width)*column+margin,
                                 (margin+cell_height)*row+margin, cell_width, cell_height])  
        FramePerSec.tick(FPS)
    pass