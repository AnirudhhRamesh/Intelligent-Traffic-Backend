#Car Model class

#global positions dictionary
from ast import Pass
from traceback import print_tb

import numpy
from passenger import Passenger

carPositions = {
    "car_1" : (0,0),
    "car_2" : (16, 16)
}

class Car:
    cellsToVisit = [] #List of cells to visit

   #Init methods 
    def __init__(self, id, socket, map):
        self.id = id
        self.isMoving = True
        self.socket = socket
        self.map = map
        self.passengers = []

    def position(self):
        return self.map.cars_positions_dict.get(self.id)

    def setTarget(self, x:int, y:int):
        self.target = (x,y)
        () #TODO: Finish dijkstra

    #Drive methods
    def stopDrive(self):
        self.isMoving=False

    def continueDrive(self):
        self.isMoving=True

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

    
#Car Attributes

#Alex writes the private methods
#Cars should have access to do the socket
#Socket is a socket object, 

#Connection outputs:

#Arduino Speed = Integer (100 - 200)
#Turning Angle = Integer ()