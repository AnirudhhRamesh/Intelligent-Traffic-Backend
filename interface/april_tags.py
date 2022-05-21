
from model.map import Map

class april_tags:

    updated_car_positions = {
        "Car1 id" : "x:23, y:46",
        "Car2 id" : "x:12, y:43"
    }

    def get_car_positions(self):
        """
        Generates the list of car positions from the camera and April tag library
        """
        #self.updated_car_positions = AprilTag.get cars
        

    def update_global_cars_positions(self):
        """
        Updates the global dict of all the cars and their positions
        """
        map.car_positions_dict = self.updated_car_positions
