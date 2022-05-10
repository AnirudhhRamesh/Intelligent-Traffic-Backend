#App.py
import socket

from model.car import Car
from model.map import Map

map_filename = "resources/map.txt"

#cars = [(bluetooth_mac, socket, carid, car),()]

def main():
    print("Starting program...")
    print()

    myMap = Map(map_filename)
    myMap.printMap()
    
    #Connect to the first car (convert this to a for loop)

    #TODO: Uncomment the two below lines to enable bluetooth running
    #cars = init_cars()
    #cars[0].setTarget(0,0)


#Initialize the car connections
def init_cars():

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

if __name__ == "__main__":
    main()


