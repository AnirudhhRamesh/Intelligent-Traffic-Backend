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
  
    def set_path(self, path):
        self.path = path
        print("PATH SET!")
        self.set_local_goal()
    
    def append_to_path(self, new_path):
        self.path.extend(new_path)
    
    def set_local_goal(self):
        print("LOCAL GOAL SET")
        if not (self.path is None) and len(self.path) > 0:
            self.local_goal = (self.path[0].x, self.path[0].y)
            self.last_goal = (self.path[len(self.path)-1].x,self.path[len(self.path)-1].y)

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
        if(not self.local_goal is None):
            dist = ((self.pos[0] - self.local_goal[0]) ** 2 + (self.pos[1] - self.local_goal[1])**2)**.5 
            print(dist)
        if (not self.local_goal is None) and ((self.pos[0] - self.local_goal[0]) ** 2 + (self.pos[1] - self.local_goal[1])**2)**.5 < .75:
            if len(self.path) > 0:
                self.path.pop(0)
            self.set_local_goal()
        if self.allowedToMove:
            if not self.local_goal is None:
                if not self.isMoving or self.sending % 5  == 0:
                    # print("driving", self.sending)
                    self.socket.send('d'.encode())
                    self.isMoving = True
                goal_vector = sub(self.local_goal,self.pos)
                car_angle = self.dir
                goal_angle = 360-angle(goal_vector[0],goal_vector[1])
                direction = dir(car_angle,goal_angle,0)
                if self.last_dir != direction or self.sending % 5 == 0:
                    self.last_dir = direction
                    print("direction", direction)
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