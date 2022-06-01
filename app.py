#App.py

from sqlite3 import adapt

import cv2
from  map import Map
import cell
import threading
from camera import Camera
from car import Car

import socket
import GUI
import threading
map_filename = "map5.csv"

#cars = [(bluetooth_mac, socket, carid, car),()]

def main():
    print("Starting program...")

    #Parse the map
    myMap = Map(map_filename)
    myMap.printMap()
    camera = Camera([4, 18, 0,6], [9, 8], myMap.max_y, myMap.max_x, myMap, goal_ids=[8])
    #cars = init_cars(myMap, camera.tr)
    #initiate GUI
    # gui = GUI.GUI(myMap)
    #Connect to the cars

    cars = init_cars(map, camera.tr)
    # april_tag_manager = april_tags()
    camera.update() #get car positions from camera and update global map 
    cars[0].position(camera.get_pos(cars[0].id))
    cars[0].direction(camera.get_dir(cars[0].id))
    cars[0].set_path(myMap.shortestPath(cars[0].get_pos(), (1,1))[1:])
    cars[1].position(camera.get_pos(cars[1].id))
    cars[1].direction(camera.get_dir(cars[1].id))
    cars[1].set_path(myMap.shortestPath(cars[1].get_pos(), (7,7))[1:])
    #TODO Alexander
    while True:
        # gui.update()
        camera.update() #get car positions from camera and update global map 
        for car in cars:
           car.position(camera.get_pos(car.id))
           car.direction(camera.get_dir(car.id))
           print(car.local_goal)
           for cell in car.path:
                i = cell.x
                j = cell.y
                cv2.circle(camera.frame_in, (int(camera.tr.inverse(i,j)[0]),int(camera.tr.inverse(i,j)[1])),5,(0,0,255),1)

        #  car.set_goal(camera.get_goal_pos(car.goal_id))
        for car in cars:
           car.drive()#find the next point in the path, and set the angle of the car to point there
        #draw
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('camera', camera.frame_in)        
    for car in cars:
        car.stopDrive()

#Initialize the car connections
def init_cars(map, tr,cars=[(9, '00:21:09:01:1e:fa'), (8, '00:21:11:02:00:0a')]):
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