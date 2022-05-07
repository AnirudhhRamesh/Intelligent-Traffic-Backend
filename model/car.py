#Car Model class

#global positions dictionary
carPositions = {
    "car_1" : (3,5),
    "car_2" : (14, 32)
}

class Car:
    
   #Init methods 
    def __init__(self, id, socket):
        self.id = id

        self.socket = socket

    def getCurrentPosition(self):
        return carPositions[id]

    def setTarget(self, x,y):
        self.target = (x,y)
        self.dijkstra() #TODO: Finish dijkstra

    #Drive methods
    def stopDrive():
        pass

    def continueDrive():
        pass

    #Path planning methods
    def dijkstra(self):
        while True:
            x = input("command: ")
            self.socket.send(x.encode())
        
        #Will calculate a path (a list of points to go to)

    
#Car Attributes

#Alex writes the private methods
#Cars should have access to do the socket
#Socket is a socket object, 

#Connection outputs:

#Arduino Speed = Integer (100 - 200)
#Turning Angle = Integer ()