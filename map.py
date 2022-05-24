from queue import Queue
from xmlrpc.client import MAXINT
import socket as Socket
from typing import Any
from direction import Direction
import car
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
        self.max_x = len(self.map)
        self.max_y = len(self.map[0])
        
        #################
        self.printMap()
        #################
        
        
        # self.cars = {
        #      "Car1 id" : car.Car("Car1 id", "car1 hardware socket", self.map),
        #      "Car2 id" : car.Car("Car2 id", "socket", self.map)
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

        for y in range(self.max_y):
            d = []
            for x in range(self.max_x):
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

    # TODO Damian
    def shortestPath(self, startCell, goalCell):
        """
        Returns a list of map cells to visit for the shortest path from the start position to the goal position
        """
        queue = Queue(self.max_x*self.max_y)
        queue.put(startCell)
        predecessors =[[None for y in range(self.max_y)] for x in range(self.max_x)] 

        while not queue.empty():
            cell = queue.get()

            for direction in cell.directions:
                newCell = None
                match direction:
                    case Direction.UP:
                        if predecessors[cell.x][min(cell.y + 1, self.max_y - 1)] is None:
                            newCell = self.map[cell.x][cell.y + 1]
                            predecessors[newCell.x][newCell.y] = cell
                            queue.put(newCell)
                            if (goalCell.x == newCell.x) and (goalCell.y == newCell.y):
                                break

                    case Direction.DOWN:
                        if predecessors[cell.x][max(0, cell.y - 1)] is None:
                            newCell = self.map[cell.x][cell.y - 1]
                            predecessors[newCell.x][newCell.y] = cell
                            queue.put(newCell)
                            if (goalCell.x == newCell.x) and (goalCell.y == newCell.y):
                                break
                    
                    case Direction.RIGHT:
                        if predecessors[min(cell.x + 1, self.max_x - 1)][cell.y] is None:
                            newCell = self.map[cell.x + 1][cell.y]
                            predecessors[newCell.x][newCell.y] = cell
                            queue.put(newCell)
                            if (goalCell.x == newCell.x) and (goalCell.y == newCell.y):
                                break

                    case Direction.LEFT:
                        if predecessors[max(0, cell.x - 1)][cell.y] is None:
                            newCell = self.map[cell.x - 1][cell.y]
                            predecessors[newCell.x][newCell.y] = cell
                            queue.put(newCell)
                            if (goalCell.x == newCell.x) and (goalCell.y == newCell.y):
                                break
        if(predecessors[goalCell.x][goalCell.y] is None):
            print("no path found........")
        
        print("goal pred", predecessors[goalCell.x][goalCell.y])
        current = goalCell
        cellsToVisit = []
        print(predecessors)
        while current != startCell:
            cellsToVisit.append(current)
            current = predecessors[current.x][current.y]

        print("")
        print("-------------------------------------")
        print(cellsToVisit)
        cellsToVisit.reverse()
        path = np.array(cellsToVisit)
        for cell in path:
            print("(", cell.x, cell.y, ")")
        # print(path)
        print("")
        return path

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

testMap = Map("map.csv")
testMap.shortestPath(testMap.map[10][4], testMap.map[12][0])
