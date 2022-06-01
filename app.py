#App.py

from sqlite3 import adapt

import cv2
import map
import cell
import threading
from camera import Camera
from car import Car

import socket
import GUI
map_filename = "map2.csv"

#cars = [(bluetooth_mac, socket, carid, car),()]

def main():
    print("Starting program...")

    #Parse the map
    myMap = map.Map(map_filename)
    myMap.printMap()
    camera = Camera([4, 18, 0,6], [9], 9, 16, goal_ids=[8])
    cars = init_cars(myMap, camera.tr)
    #initiate GUI
    gui = GUI.GUI(myMap)
    #Connect to the cars
    #init_cars()
    #april_tag_manager = april_tags()

    #Add passenger (TODO Use gui/separate thread to listen for inputs)
    # newPassenger = passenger.Passenger(myMap.getCell(0,0), myMap.getCell(0, 0))
    # myMap.add_passenger(newPassenger)

    #TODO Alexander
    while True:
        gui.update()
        camera.update() #get car positions from camera and update global map 
        for car in cars:
           car.position(camera.get_pos(car.id))
           car.direction(camera.get_dir(car.id))
           car.set_goal(camera.get_goal_pos(car.goal_id))
        for car in cars:
           car.drive()#find the next point in the path, and set the angle of the car to point there
        #draw
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('camera', camera.frame_in)        
    for car in cars:
        car.stopDrive()

#Initialize the car connections
def init_cars(map, tr,cars=[(9, '00:21:09:01:1e:fa')]):
    car_list = []
    for car in cars:
        adapter_addr = car[1]
        port = 1
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.connect((adapter_addr, port))
        print(s)
        newCar = Car(car[0], s, map, tr)
        car_list.append(newCar)
    return car_list

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