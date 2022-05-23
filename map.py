import socket
from direction import Direction
import traffic_engine
import car
from cell import Cell
import passenger

#Map definition
class Map:

    passengers = []

    #List of all the cars and their positions
    cars_positions_dict = {
        "Car1 id" : (23, 43),
        "Car2 id" : (12, 46)
    }


    def __init__(self, filename) -> None:
        #Parse the file and generate the map
        self.filename = filename
        self.map = self.parseFile(filename)
        self.cars = {
        "Car1 id" : car.Car("Car1 id", "car1 hardware socket", self.map),
        "Car2 id" : car.Car("Car2 id", "socket", self.map)
    }

    def add_passenger(self, passenger:passenger.Passenger) -> None:
        """
        Add a passenger to a specific map cell and assign the passenger to a car
        """
        self.passengers.append(passenger)


    def shortestPath(map, startCell, goalCell):
        """
        Returns a list of map cells to visit for the shortest path from the start position to the goal position
        
        Parameters
        ----------
        startCell: Cell
            The start cell of the path
        goalCell: Cell
            The end cell of the path
        """
        while False:
            pass
        
        listOfCellsToVisit = []
        return listOfCellsToVisit

    def initSingleSource(G, s):
        #Init-single-source(G, s): -> G, s

        pass

    def getCell(self, x:int, y:int):
        """
        Returns the cell of the corresponding x and y values
        """
        return self.map[x][y] #TODO: Make sure map representation is correct, maybe translation method required?


    ## Helper methods ##

    #Convert text file to 2D enum array: x, y, true or false, UP/RIGHT/DOWN/LEFT
    def parseFile(self, filename:str):

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

                    newCell = Cell(int(x), int(y), isRoad.lower() == "true", parsedDirectionsList)
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