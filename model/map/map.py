from socket import socket
from xmlrpc.client import MAXINT
from model.Direction import Direction
from engine.traffic_engine import traffic_engine
from model.car import Car

#Map definition
class Map:
    print("hello")

    passengers = []

    #List of all the cars and their positions
    cars_positions_dict = {
        "Car1 id" : (23, 43),
        "Car2 id" : (12, 46)
    }

    #List of the car representation and their ids
    cars = {
        "Car1 id" : Car("Car1 id", "car1 hardware socket"),
        "Car2 id" : Car("Car2 id", "socket")
    }

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
              #  splitLines = line.split(' ')
                cells = line.split(',')
                newMapRow = []
               # for row in splitLines:
                for cell in cells:
                #    (x, y, isRoad, Directions) = row.split(',')
                    # directionsList = Directions.split('/')
                    if cell.lower() == "x":
                        newCell = self.Cell(int(x), int(y), False, parsedDirectionsList)
                    else:
                        parsedDirectionsList = []
                        for direction in cell.split('/'):
                            if direction.lower() == "up": parsedDirectionsList.append(Direction.UP)
                            if direction.lower() == "right": parsedDirectionsList.append(Direction.RIGHT)
                            if direction.lower() == "down": parsedDirectionsList.append(Direction.DOWN)
                            if direction.lower() == "left": parsedDirectionsList.append(Direction.LEFT)
                            
                            newCell = self.Cell(int(x), int(y), True, parsedDirectionsList)
                            
                    newMapRow.append(newCell)
                    x += 1
                newMap.append(newMapRow)
                y += 1

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

    def add_passenger(self, x, y):
        """
        Add a passenger to a specific map cell and assign the passenger to a car
        """
        newPassenger = self.Passenger(x,y)
        self.passengers.append(newPassenger)
        traffic_engine.assign_passenger(newPassenger)

    def shortest_path_recur(self, currentCell, goalCell, visited, pathLength):
        if currentCell == goalCell:
            return (visited, pathLength)
        
        directions = currentCell.getDirections()
        paths = []
        lengths = []

        for direction in directions:
            if not visited.contains(direction.cell):
                temp = shortest_path_recur(direction.cell, goalCell, visited.add(currentCell), pathLength+1)    #direction.cell should be the neighbor cell in corresponding direction
                paths.append(temp)
                lengths.append(temp._2)

        shortestLength = min(lengths)

        return paths[lengths.index(shortestLength)]


    def shortestPath(self, startCell, goalCell):
        """
        Returns a list of map cells to visit for the shortest path from the start position to the goal position
        """
        while False:
            pass

        listOfCellsToVisit = shortest_path_recur(startCell, goalCell, [], MAXINT)
        return listOfCellsToVisit

    


    def initSingleSource(G, s):
        #Init-single-source(G, s): -> G, s

        pass
