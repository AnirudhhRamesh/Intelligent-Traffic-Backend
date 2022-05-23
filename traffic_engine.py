#Traffic engine definition: Decides and performs intelligent traffic
from typing import Any
import car
import map

class Traffic_Engine:
    
    def __init__(self, map):
        self.map = map
    
    def assign_passenger(self, passenger) -> None:
        """
        Add a new passenger to the map and assign it to a car
        """
        self.traffic_controller(passenger)

    def traffic_controller(self, passenger) -> None:
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
        for (carId, car) in self.map.cars.items():
            print(f"Map type: {type(self.map)}")
            newPath = len(map.Map.shortestPath(self.map, car.lastPassenger, passenger))
            if shortestPath > newPath:
                shortestPath = newPath
                shortestPathCar = car

        shortestPathCar.add_passenger_destination(passenger)