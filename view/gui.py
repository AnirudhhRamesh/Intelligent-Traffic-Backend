import pygame
from pygame.locals import *

	
 
 
# pygame.draw.polygon(surface, color, pointlist, width)
# pygame.draw.line(surface, color, start_point, end_point, width)
# pygame.draw.lines(surface, color, closed, pointlist, width)
# pygame.draw.circle(surface, color, center_point, radius, width)
# pygame.draw.ellipse(surface, color, bounding_rectangle, width)
# pygame.draw.rect(surface, color, rectangle_tuple, width)


#GUI description
class GUI:


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


    # window size
    DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
    DISPLAYSURF.fill(WHITE)
    
    pygame.draw.line(DISPLAYSURF, BLACK, (0, 0), (MAX_X, 0))
    pygame.draw.line(DISPLAYSURF, BLACK, (0, 0), (0, MAX_Y))
    pygame.draw.line(DISPLAYSURF, BLACK, (MAX_X, 0), (MAX_X, MAX_Y))
    pygame.draw.line(DISPLAYSURF, BLACK, (0, MAX_Y), (MAX_X, MAX_Y))

    #Game loop begins
    while True:
        # Code


        pygame.draw.circle(DISPLAYSURF, BLACK, (200,50), 30)

        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        FramePerSec.tick(FPS)



    pass