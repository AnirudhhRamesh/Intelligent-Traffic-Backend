from xmlrpc.client import MAXINT
import socket as Socket
from typing import Any
from direction import Direction
import car as Car
from cell import Cell
import passenger as Passenger
import numpy as np



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
        #self.map = self.parseFile("map.txt")
        self.map = self.parseFile(filename)
        self.maxX = len(self.map)
        self.maxY = len(self.map[0])
        
        #################
        self.printMap()
        #################
        
        
        # self.cars = {
        #     "Car1 id" : Car("Car1 id", "car1 hardware socket", self.map),
        #     "Car2 id" : Car("Car2 id", "socket", self.map)
        # }
        
    


    def getDirection(self, direction):
        if direction.lower() == "up": 
            return Direction.UP
        elif direction.lower() == "right": 
            return Direction.RIGHT
        elif direction.lower() == "down": 
            return Direction.DOWN
        else: #direction.lower() == "left": 
            return Direction.LEFT

    def parseFile(self, filename):

        #2D array of all the cells
        newMap = []

        with open(filename, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()

            x = 0
            y = 0
            
            max_y = len(lines)
            max_x = len(lines[0].split(','))
            
            lines.reverse()
            newMap = [[None for y in range(max_y)] for x in range(max_x)] 
            for line in lines:
                cells = line.split(',')
                
                
                for cell in cells:
                    cell = cell.strip()
                    # newCell = None
                                        
                    if cell.lower() == "x":
                        newMap[x][y] = Cell(int(x), int(y), False, [])
                        # newCell = "X"
                    else:
                        parsedDirectionsList = []
                        directions = cell.split('/')
                        for direction in directions:
                            parsedDirectionsList.append(self.getDirection(direction))
                            
                        newMap[x][y] = Cell(int(x), int(y), True, parsedDirectionsList)
                    x += 1
                # newMap.append(newMapRow)
                y += 1
                x = 0
            f.close()

            m = np.array(newMap)
        return m


    # #Convert text file to 2D enum array: x, y, true or false, UP/RIGHT/DOWN/LEFT
    # def parseFile(self, filename):
    def printMap(self):
        array = []
        
        max_y = len(self.map[0])
        max_x = len(self.map)
        for y in range(max_y):
            d = []
            for x in range(max_x):
                cell = self.map[x][y]
                dirString = ""
                directions = cell.directions
                length = len(directions)
                if length == 0:
                    dirString = " XX "
                else:                       
                    for dir in directions:
                        dirString += Direction.toString(dir)
                    match length:
                        case 1:
                            dirString = " " + dirString + "  "
                        case 2:
                            dirString = " " + dirString + " "
                        case 3:
                            dirString += " "
                d.append(dirString)
            array.append(d)
            
        numpyMap = np.array(array)
        
        print(np.array2string(numpyMap, separator=' | '))
                
                
            
            

    def add_passenger(self, passenger):
        """
        Add a passenger to a specific map cell and assign the passenger to a car
        """
        self.passengers.append(passenger)
        self.assign_passenger(passenger)

    #TODO Damian
    def shortest_path_recur(self, currentCell, goalCell, visited, pathLength):
        """
        if currentCell == goalCell:
            return (visited, pathLength)
        
        directions = currentCell.getDirections()
        paths = []
        lengths = []

        for direction in directions:
            if not visited.contains(direction.cell):
                temp = self.shortest_path_recur(direction.cell, goalCell, visited.add(currentCell), pathLength+1)    #direction.cell should be the neighbor cell in corresponding direction
                paths.append(temp)
                lengths.append(temp._2)

        shortestLength = min(lengths)

        return paths[lengths.index(shortestLength)]
        """
        pass

    # TODO Damian
    def shortestPath(self, startCell, goalCell):
        """
        Returns a list of map cells to visit for the shortest path from the start position to the goal position
        """
        while False:
            pass

        listOfCellsToVisit = []#self.shortest_path_recur(startCell, goalCell, [], MAXINT)
        return listOfCellsToVisit

    def getCell(self, x, y):
        return self.map[x][y]


    def assign_passenger(self, passenger) -> None:
        """
        Assigns a newly generated passenger to the car whose last destination is closest to the passenger cell
        """
        shortestPath = 10000
        shortestPathCar = Any

        #TODO Alexander
        #for car in cars:
        #    for car2 in cars:
        #        if car != car2:
        #            if car is in front of car2
        #                car2.stop()

        #Find the car with the shortest path to the next passenger
        for (carId, car) in self.cars.items():
            print(f"Map type: {type(self.map)}")
            newPath = len(self.shortestPath(car.lastPassenger.goal, passenger.start))
            if shortestPath > newPath:
                shortestPath = newPath
                shortestPathCar = car

        shortestPathCar.add_passenger_destination(passenger)
    
    def initSingleSource(G, s):
        #Init-single-source(G, s): -> G, s

        pass