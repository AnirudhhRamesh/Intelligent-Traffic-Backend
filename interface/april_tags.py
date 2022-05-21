
from model.map.map import Map

class april_tags:

    updated_car_positions = {
        "Car1 id" : "x:23, y:46",
        "Car2 id" : "x:12, y:43"
    }

    def update_car_positions(self):
        """
        Generates the list of car positions from the camera and April tag library
        """
        #self.updated_car_positions = AprilTag.get cars
        
        Map.cars_positions_dict = self.updated_car_positions
        
        pass