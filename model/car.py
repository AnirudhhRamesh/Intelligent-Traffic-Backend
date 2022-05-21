#Car Model class
from model.map import Map

#global positions dictionary
carPositions = {
    "car_1" : (3,5),
    "car_2" : (14, 32)
}

class Car:
    
    passengers = [] #List of passenger cells to visit
    cellsToVisit = [] #List of cells to visit

   #Init methods 
    def __init__(self, id, socket):
        self.id = id

        self.socket = socket

    def position(self):
        return Map.cars_positions_dict.get(self.id)

    def setTarget(self, x,y):
        self.target = (x,y)
        () #TODO: Finish dijkstra

    #Drive methods
    def stopDrive():
        pass

    def continueDrive():
        pass

    #Updates the car
    def update():
        local_goal = cellsToVisit[0]
        if(near local_goal):
            cellsToVist.pop()
        else:
            adjust_angle()

        
        pass
    
    def add_passenger_destination(self, newPassenger):
        """
        Adds the given passenger to the car's list of passengers.
        Appends the shortest path from the last passenger to the newly added passenger to the car's cellsToVisit
        """
        self.passengers.append(newPassenger)
        self.cellsToVisit.append(map.shortestPath(self.lastPassenger, newPassenger))
    
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