
from passenger import Passenger


class Cell:
    def __init__(self, x, y, isRoad, directions):
        self.x = x
        self.y = y
        
        self.isRoad = isRoad
        self.directions = directions
        self.passenger : Passenger = None 

    def getDirections(self):
        self.directions
    
    def position(self):
        return (self.x, self.y)

    def hasPassenger(self):
        return self.passenger is not None