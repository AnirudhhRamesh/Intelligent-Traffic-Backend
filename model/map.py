import Direction

#Map definition
class Map:    
    class Cell:
        def __init__(self, x, y, directions, isRoad):
            self.x = x
            self.y = y
            
            self.directions = directions
            self.isRoad = isRoad

        def getDirections(self):
            if (self.isRoad):
                #Return the cell directions
                pass
            else:
                #Return empty list
                pass

    def __init__(self, filename):
        #Parse the file and generate the map
        self.filename = filename
        self.map = parseFile(filename)

    def parseFile(filename):
        #Convert text file to 2D enum array
        pass

    def shortestPath(startX, startY, endX, endY):
        #Given positions, find the shortest path on the map, or returns null if unkown
        pass

    cell1 = Cell(2, 3, [Direction.DOWN])
    cell2 = Cell(3,4,[Direction.Left, Direction.Down])
    

    allmaps = [cell1, cell2]

