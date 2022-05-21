#App.py
import socket
from interface.april_tags import april_tags

from model.car import Car
from model.map import Map

map_filename = "resources/map.txt"

#cars = [(bluetooth_mac, socket, carid, car),()]

def main():
    print("Starting program...")
    print()

    #Parse the map
    myMap = Map(map_filename)
    myMap.printMap()
    
    #Connect to the cars
    init_cars()
    april_tag_manager = april_tags()

    #Add passenger (TODO Use gui/separate thread to listen for inputs)
    myMap.add_passenger(Map.Passenger(12,13))

    while True:
        april_tag_manager.update_car_positions
        


#Initialize the car connections
def init_cars():
    pass

    """
    #Initialize the first car
    #Address of the first car
    adapter_addr = '00:21:11:01:FA:1C' #car_1 bluetooth mac address
    port = 1 #Computer bluetooth port

    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) #Make one for every car

    s.connect((adapter_addr, port))
    
    car1 = Car(97, s)
    
    return [car1]
    #while True:
    #    x = input("command: ")
    #    s.send(x) #send stop to car. Car arduino will loop through instructions
    """

if __name__ == "__main__":
    main()


