from model.Direction import Direction

#Map definition
class Map:
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

    def __init__(self, filename):
        #Parse the file and generate the map
        self.filename = filename
        self.map = self.parseFile(filename)

    #Convert text file to 2D enum array: x, y, true or false, UP/RIGHT/DOWN/LEFT
    def parseFile(self, filename):

        #2D array of all the cells
        newMap = []

        with open(filename, 'r') as f:
            lines = f.readlines()

            x = 0
            y = 0

            #Iterate through each line of map
            for line in lines:
                splitLines = line.split(' ')
                newMapRow = []
                for row in splitLines:
                    (x, y, isRoad, Directions) = row.split(',')
                    directionsList = Directions.split('/')

                    parsedDirectionsList = []
                    for direction in directionsList:
                        if direction.lower() == "up": parsedDirectionsList.append(Direction.UP)
                        if direction.lower() == "right": parsedDirectionsList.append(Direction.RIGHT)
                        if direction.lower() == "down": parsedDirectionsList.append(Direction.DOWN)
                        if direction.lower() == "left": parsedDirectionsList.append(Direction.LEFT)

                    newCell = self.Cell(int(x), int(y), isRoad.lower() == "true", parsedDirectionsList)
                    newMapRow.append(newCell)
                newMap.append(newMapRow)

            f.close()
        
        return newMap

    def printMap(self):
        for x in range(len(self.map)):
            for y in self.map[x]:
                cellX = y.x
                cellY = y.y
                cellIsRoad = y.isRoad
                cellDirections = y.directions
                print(f"Cell: ({cellX}, {cellY}) : {cellIsRoad} and {cellDirections}")
            print()

    #Dijkstra: Given positions, find the shortest path on the map, or returns null if unkown
    def shortestPath(startX, startY, endX, endY):
        #Dijkstra(G, w, s): G->map, w->edge-weight, s->startPos
        pass

    def initSingleSource(G, s):
        #Init-single-source(G, s): -> G, s

        pass