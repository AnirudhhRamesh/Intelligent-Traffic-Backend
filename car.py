#Car Model class

#global positions dictionary
from ast import Pass
from re import S
from traceback import print_tb
from turtle import pos
from car_commands import *
import numpy
from cell import Cell
from passenger import Passenger



class Car:

   #Init methods 
    def __init__(self, id, socket, map,tr):
        #FOR TESTING ONLY, REMOVE LATER
        self.goal_id = 8
        self.sending = 0
        self.id = id
        self.tr = tr
        self.isMoving = False
        self.allowedToMove = True
        self.socket = socket
        self.socket.send('g'.encode())
        self.last_dir = 'g'
        self.socket.send('h'.encode())
        self.map = map
        self.dir = 0
        self.pos = (0,0)
        self.passengers = []
        self.currentPassenger: Passenger = None
        self.cellsToVisit = [] #List of cells to visit

    def set_goal(self,goal):
        self.goal = goal
    def position(self, pos):
        self.pos = pos
    def direction(self, dir):
        self.dir = dir
    def setTarget(self, x,y):
        self.target = (x,y)
        #TODO: Finish dijkstra

    #Drive methods
    def stopDrive(self):
        self.allowedToMove=False
        if self.isMoving:
            self.socket.send('h'.encode())
            self.isMoving = False
    def continueDrive(self):
        self.allowedToMove=True


    def drive(self):
        if self.allowedToMove:
            if not self.isMoving:
                self.socket.send('d'.encode())
                self.isMoving = True
            # print(self.goal, self.pos)
            goal_vector = sub(self.goal,self.pos)
            # current_vector = self.dir
            car_angle = self.dir
            print(car_angle)
            goal_angle = 360-angle(goal_vector[0],goal_vector[1])
            direction = dir(car_angle,goal_angle,0)
            # print(direction)
            if self.last_dir != direction or self.sending % 5 == 0:
                self.last_dir = direction
                self.sending = (self.sending + 1) % 5
                self.socket.send(direction.encode())
        else:
            if self.isMoving:
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
        print(type(path))
        print(type(self.cellsToVisit))
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
    
    def checkIfPassengerOnCells(self):
        currentCell: Cell = self.map.getCell(self.pos[0], self.pos[1])
        if(currentCell.hasPassenger() and currentCell.passenger in self.passengers):
            self.currentPassenger = currentCell.passenger
            currentCell.passenger.inCar = True
            currentCell.passenger = None

    def CheckIfOnDestination(self):
        currentCell: Cell = self.map.getCell(self.pos[0], self.pos[1])
        if(currentCell == self.currentPassenger.goal):
            self.currentPassenger = None
            

    
#Car Attributes

#Alex writes the private methods
#Cars should have access to do the socket
#Socket is a socket object, 

#Connection outputs:

#Arduino Speed = Integer (100 - 200)
#Turning Angle = Integer ()