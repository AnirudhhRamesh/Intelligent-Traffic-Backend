#Traffic engine definition: Decides and performs intelligent traffic


from model.car import Car
from model.map.map import Map

class traffic_engine:
    
    def assign_passenger(self, passenger):
        """
        Add a new passenger to the map and assign it to a car
        """
        self.intelligent_decision_maker(passenger)

    def intelligent_decision_maker(self, passenger):
        """
        Assigns a newly generated passenger to the car whose last destination is closest to the passenger cell
        """

        shortestPath = 10000
        shortestPathCar

        #TODO Alexander
        #for car in cars:
        #    for car2 in cars:
        #        if car != car2:
        #            if car is in front of car2
        #                car2.stop()

        #Find the car with the shortest path to the next passenger
        for (carId, car) in Map.cars.items():
            newPath = len(Map.shortestPath(car.lastPassenger.position, passenger.position))
            if shortestPath > newPath:
                shortestPath = newPath
                shortestPathCar = car

        shortestPathCar.add_passenger_destination(passenger)