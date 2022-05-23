
class Cell:
    def __init__(self, x, y, isRoad, directions):
        self.x = x
        self.y = y
        
        self.isRoad = isRoad
        self.directions = directions

    def getDirections(self):
        if (self.isRoad):
            #Return the cell directions
            pass
        else:
            #Return empty list
            pass
    
    def position(self):
        return (self.x, self.y)