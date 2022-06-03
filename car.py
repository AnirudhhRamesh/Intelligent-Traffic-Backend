#Car Model class

#global positions dictionary
# from ast import Pass
# from re import S
from traceback import print_tb
# from turtle import pos

# from torch import R
from car_commands import *
import numpy
from cell import Cell
from passenger import Passenger


CURVE_TRANSLATION = 0.25

class Car:

   #Init methods 
    def __init__(self, id, socket,color):
        #FOR TESTING ONLY, REMOVE LATER
        self.goal_id = 8
        self.sending = 0
        self.color = color
        self.id = id
        self.path = None
        self.isMoving = False
        self.allowedToMove = True
        self.socket = socket
        #self.socket.send('g'.encode())
        self.last_dir = 'g'
        #self.socket.send('h'.encode())
        self.dir = 0
        self.local_goal = None
        self.pos = None
        self.passengers = []
        self.currentPassenger: Passenger = None
        self.cellsToVisit = [] #List of cells to visit
        self.last_goal = self.pos
        
        # contains the translation for the coordinates (always zero, except in the curves...)
        # self.translateCorners = self.computeTranslate()
  
  
    def computeTranslate(self, path):
        translations = []
        translations.append((0,0))
        for i in range(1, len(path)-1):
            translations.append(self.curveTranslate(path, i))
            
        translations.append((0,0))
        self.translations = translations
            
                
        
    def curveTranslate(self, path, i): #returns (x,y) translate (if not curve, (0,0))
        
        if 0 < i and i < len(path) - 1:
            (x0, y0) = (path[i-1].x, path[i-1].y)
            (x1, y1) = (path[i].x, path[i].y)
            (x2, y2) = (path[i+1].x, path[i+1].y)
            
            #check for double curve:
            if i < len(path) - 2:
                (x3, y3) = (path[i+2].x, path[i+2].y)
                if x0 == x1 and y1 == y2 and (x3 == x0 or y3 == y0):
                    return (0,0)
                elif y0 == y1 and x1 == x2 and (x3 == x0 or y3 == y0):
                    return (0,0)
            
            # up (left/right) / down(left/right)
            if x0 == x1 and y1 == y2:
                if y0 < y1: #up:
                    if x1 < x2: #right
                        return (CURVE_TRANSLATION, -CURVE_TRANSLATION)
                    else: # left
                        return (-CURVE_TRANSLATION, -CURVE_TRANSLATION)
                else: #down:
                    if x1 < x2: #right
                        return (CURVE_TRANSLATION, CURVE_TRANSLATION)
                    else: # left
                        return (-CURVE_TRANSLATION, CURVE_TRANSLATION)
                
            # left (up/down) / right (up/down)
            elif y0 == y1 and x1 == x2:
                if x0 < x1: #right:
                    if y1 < y2: #up
                        return (-CURVE_TRANSLATION, CURVE_TRANSLATION)
                    else: # down
                        return (-CURVE_TRANSLATION, -CURVE_TRANSLATION)
                else: #left:
                    if y1 < y2: #up
                        return (CURVE_TRANSLATION, CURVE_TRANSLATION)
                    else: # down
                        return (CURVE_TRANSLATION, -CURVE_TRANSLATION)
            else:
                return (0,0)
        else:
            return (0,0)
                
            
            
            # check  transpose down & l/r
            
            # check  transpose up & l/r
            
  
    def set_path(self, path):
        self.path = path
        self.computeTranslate(path)
        self.set_local_goal()
        
    
    def set_local_goal(self):

        if not (self.path is None) and len(self.path) > 0:
            print("translation", self.translations[len(self.translations)-1])
            self.local_goal = (self.path[0].x + self.translations[0][0], self.path[0].y + self.translations[0][1]) 
            self.last_goal = (self.path[len(self.path)-1].x + self.translations[len(self.translations)-1][0],self.path[len(self.path)-1].y + self.translations[len(self.translations)-1][1])
            
            
            
            for i in range(len(self.path)):
                print("normal: (", self.path[i].x, ", ", self.path[i].y, "),  actual: (", self.path[i].x + self.translations[i][0], ", ", self.path[i].y + self.translations[i][1], ")")
                
             

            self.drive()
            
        else: 
            self.local_goal = self.get_pos()
            self.stopDrive()
    def position(self, pos):
        self.pos = pos
        if self.path is None:
            self.last_goal = self.get_pos()
    def direction(self, dir):
        self.dir = dir
    def get_pos(self):
        return (int(self.pos[0]), int(self.pos[1]))
    
        #TODO: Finish dijkstra

    #Drive methods
    def stopDrive(self):
        self.allowedToMove=False
        if self.isMoving:
            # print("stopping!")
            self.socket.send('h'.encode())
            self.isMoving = False
    def continueDrive(self):
        self.allowedToMove=True


    def drive(self):
        self.sending = (self.sending + 1) % 5

        if (not self.local_goal is None) and ((self.pos[0] - self.local_goal[0]) ** 2 + (self.pos[1] - self.local_goal[1])**2)**.5 < .75:
            if len(self.path) > 0:
                self.path.pop(0)
                self.translations.pop(0)
            self.set_local_goal()
        if self.allowedToMove:
            if not self.local_goal is None:
                if not self.isMoving or self.sending % 5  == 0:
                    # print("driving", self.sending)
                    self.socket.send('d'.encode())
                    self.isMoving = True
                goal_vector = sub(self.local_goal,self.pos) #local goal
                car_angle = self.dir
                goal_angle = 360-angle(goal_vector[0],goal_vector[1])
                direction = dir(car_angle,goal_angle,0)
                if self.last_dir != direction or self.sending % 5 == 0:
                    self.last_dir = direction
                    self.socket.send(direction.encode())
        else:
            if self.isMoving:
                print("stop from that other place (line 96)")
                self.socket.send('h'.encode())
                self.isMoving = False
        
    #Updates the car's driving angle and moves the car 
    #TODO Alexander
    #def update():
    #    if self.isMoving:
    #        socket.send('d')
    #    else:
    #        socket.send('s')
    #    local_goal = cellsToVisit[0]
    #    if(near local_goal):
    #        cellsToVist.pop()
    #    else:
    #        adjust_angle()   
    #    pass
    
    def add_passenger_destination(self, newPassenger: Passenger, path):
        """
        Adds the given passenger to the car's list of passengers.
        Appends the shortest path from the last passenger to the newly added passenger to the car's cellsToVisit
        """
        self.passengers.append(newPassenger)
        self.cellsToVisit += path
    
    def lastPassenger(self):
        """
        Returns the last passenger the car will visit
        """
        return self.passengers[-1]
    
    def cells_to_visit_count(self):
        """
        Returns the total cells the car has to visit
        """
        return len(self.passengers)

    
#Car Attributes

#Alex writes the private methods
#Cars should have access to do the socket
#Socket is a socket object, 

#Connection outputs:

#Arduino Speed = Integer (100 - 200)
#Turning Angle = Integer ()