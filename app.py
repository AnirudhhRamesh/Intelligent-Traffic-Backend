#App.py
import traffic_engine
import april_tags

import map
import cell
import passenger

import car
map_filename = "map.txt"

#cars = [(bluetooth_mac, socket, carid, car),()]

def main():
    print("Starting program...")
    print()

    #Parse the map
    myMap = map.Map(map_filename)
    myMap.printMap()
    
    myTrafficEngine = traffic_engine.Traffic_Engine(myMap)

    #Connect to the cars
    #init_cars()
    #april_tag_manager = april_tags()

    #Add passenger (TODO Use gui/separate thread to listen for inputs)
    newPassenger = passenger.Passenger(myMap.getCell(0,0), myMap.getCell(0, 0))
    myMap.add_passenger(newPassenger)
    myTrafficEngine.assign_passenger(newPassenger)

    #TODO Alexander
    #while True:
        #april_tag_manager.update_car_positions #get car positions from camera and update global map 
        #traffic_engine.accept_new_passengers() #accept new passengers and add points to cars' paths 
        #for each car in cars: 
        #    car.update()#find the next point in the path, and set the angle of the car to point there

        


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


