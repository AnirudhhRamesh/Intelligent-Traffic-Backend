import cv2
import random

from cv2 import sqrt

STOP_SIGN_DIST = 3

class DecisionMaker:
    def __init__(self,cars,map,camera):
        self.cars = cars
        self.myMap = map
        self.queue = [[],[],[],[],[]]
        self.allowedToGo = [[],[],[],[],[]]
        self.camera = camera

    def update(self, camera):
        self.camera = camera
        for car in self.cars:
            car.position(camera.get_pos(car.id))
            car.direction(camera.get_dir(car.id))
            if car.path is None or len(car.path) == 0:
                ng = (0,0)
                while True:
                    x = random.randint(0, self.myMap.max_x-1)
                    y = random.randint(0, self.myMap.max_y-1)
                    ng = (x,y)
                    if(self.myMap.getCell(x,y).isRoad):
                        break
                car.set_path(self.myMap.shortestPath(car.last_goal, ng))
                car.continueDrive()
            for cell in car.path:
                i = cell.x
                j = cell.y
                cv2.circle(camera.frame_in, (int(camera.tr.inverse(i,j)[0]),int(camera.tr.inverse(i,j)[1])),5,(0,0,255),1)

        self.intersection(5,1,0)
        self.intersection(1,5,1)
        self.intersection(5,5,2)
        self.intersection(9,5,3)
        self.intersection(5,9,4)
 
    def distance(self,x1,y1,x2,y2):
        return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    

    def intersection(self,centerX,centerY,id):
        cv2.circle(self.camera.frame_in, (int(self.camera.tr.inverse(centerX,centerY)[0]),int(self.camera.tr.inverse(centerX,centerY)[1])),30,(0,0,255),1)
        for car in self.cars:
            if(self.distance(car.pos[0], car.pos[1], centerX,centerY) < STOP_SIGN_DIST and not self.allowedToGo[id].includes(car)):
                car.stopDrive()
                if not self.queue[id].includes(car):
                    self.queue[id].push(car)
                
        #let car go if no one is intersection 
        if self.queue[id].length > 0 :
            if(self.allowedToGo[id].length == 0):
                goCar = self.queue[id].shift()
                self.allowedToGo[id].push(goCar)
                # goCar.continue()
                goCar.continueDrive()
                
            
        #let car go if it can go
        if self.allowedToGo[id].length > 0 and self.queue[id].length > 0:
            for i in range(min(2,self.queue[id].length)):
                canGo = True
                for j in range(self.allowedToGo[id].length):
                    # console.log(self.queue[id][i], self.allowedToGo[id][j])
                    if(self.queue[id][i].pathCrosses(self.allowedToGo[id][j],3)):
                        # //console.log("------------------------------------------------")
                        canGo = False
                    
                    
                
            #    // console.log(canGo)
                if(canGo):
                    goCar = self.queue[id].shift()
                    self.allowedToGo[id].push(goCar)
                    # goCar.continue()
                    goCar.continueDrive()

                # //   console.log("can drive!!!!!!!!!!!!!!!! ",canGo)
                # //   console.log(goCar)
            #    // console.log("hello")
        
        # self.allowedToGo[id] =  self.allowedToGo[id].filter(lambda: car => dist(car.x, car.y,centerX, centerY) < STOP_SIGN_DIST)

        for car in self.cars:
            if self.distance(car.pos[0], car.pos[1],centerX, centerY) < STOP_SIGN_DIST:
                self.allowedToGo[id] = car