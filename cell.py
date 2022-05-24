
class Cell:
    def __init__(self, x, y, isRoad, directions):
        self.x = x
        self.y = y
        
        self.isRoad = isRoad
        self.directions = directions
        self.hasPassenger = False

    def getDirections(self):
        self.directions
    
    def position(self):
        return (self.x, self.y)