#App.py

from sqlite3 import adapt
import cv2
from scipy.fft import idct
from direction import Direction
from  map import Map
import cell
import threading
from decision_maker import DecisionMaker
from camera import Camera
from car import Car
import traceback
import socket
import GUI
import threading
map_filename = "map5.csv"
car_list = [
    #(9,'00:21:11:01:FA:14', (255,0,0)),
(8, '00:21:11:01:FA:1C', (0,255,0))
# (10, '00:21:09:01:1e:fa')
#  '00:21:09:01:1e:fa'
]
#cars = [(bluetooth_mac, socket, carid, car),()]

def main():
    print("starting program...")

    #Parse the map
    cars = init_cars(car_list)

    myMap = Map(map_filename, cars)
    #myMap.printMap()
    camera = Camera([4, 18, 0,6], [9,8], myMap.max_y, myMap.max_x, myMap)
    #dm = DecisionMaker(cars, myMap,camera)
    #Wait for camera to initialize 
    print("searching for corners...")
    while not camera.tr.foundCorners():
        camera.update()
    print("found corners!")
    print("searching for cars...")
    #TODO: wait for cars positions to be found 
    foundAllCars = False
    while not foundAllCars:
        foundAllCars = True
        camera.update()
        for (id,mac,color) in car_list:
            if camera.get_pos(id) is None:
                foundAllCars = False
    print("found all cars!")
    #at this point all cars should have their position updated
        
    for car in cars:
        car.position(camera.get_pos(car.id))
        car.direction(camera.get_dir(car.id))


    #initiate GUI
    gui = GUI.GUI(myMap)
    gui.launchGUI()

   
    #TODO Alexander
    try:
        while True:
            gui.update()
            camera.update() #get car positions from camera and update global map 
            #dm.update(camera)
            for car in cars:
                car.position(camera.get_pos(car.id))
                car.direction(camera.get_dir(car.id))
                if not car.path is None:
                    for cell in car.path:
                        i = cell.x
                        j = cell.y
                        for passenger in car.passengers:
                            if(cell == passenger.start):
                               cv2.circle(camera.frame_in, (int(camera.tr.inverse(i,j)[0]),int(camera.tr.inverse(i,j)[1])),car.id,(0,0,255),1)
                            elif(cell == passenger.goal):
                                cv2.circle(camera.frame_in, (int(camera.tr.inverse(i,j)[0]),int(camera.tr.inverse(i,j)[1])),car.id,(255,255,0),1)
                            else:       
                                cv2.circle(camera.frame_in, (int(camera.tr.inverse(i,j)[0]),int(camera.tr.inverse(i,j)[1])),car.id,car.color,1)
                car.drive() #find the next point in the path, and set the angle of the car to point there
            # draw
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow('camera', camera.frame_in)      
    except Exception as e:  
        tb = traceback.format_exc()
        print("-------ERROR-------")
        print(e)
        print(tb)
    finally:
        for i in range(40):
            for car in cars:
                car.stopDrive()
#Initialize the car connections
def init_cars(cars):
    car_list = []
    for car in cars:
        adapter_addr = car[1]
        port = 1
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.connect((adapter_addr, port))
        # print(s)
        newCar = Car(car[0], s, car[2])
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