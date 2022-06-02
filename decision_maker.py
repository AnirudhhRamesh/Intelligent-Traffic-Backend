import cv2
import random

from cv2 import sqrt

STOP_SIGN_DIST = 1.4

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
                cv2.circle(camera.frame_in, (int(camera.tr.inverse(i,j)[0]),int(camera.tr.inverse(i,j)[1])),car.id,car.color,1)

        # self.intersection(6.5,3.5,0)
        # self.intersection(3.5,6.5,1)
        # self.intersection(3.5,3.5,2)
        # self.intersection(2.5,2.5,2)
        # self.intersection(.5,3.5,3)
        # self.intersection(3.5,.5,4)
        for i in range(len(self.myMap.intersections)):
            self.intersection(self.myMap.intersections[i][0], self.myMap.intersections[i][1], i)
 
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))**.5
    

    def intersection(self,centerX,centerY,id):
        # print(self.queue[id])
        radius = int((self.camera.tr.inverse(STOP_SIGN_DIST,STOP_SIGN_DIST)[0])*.25)
        cv2.circle(self.camera.frame_in, (int(self.camera.tr.inverse(centerX,centerY)[0]),int(self.camera.tr.inverse(centerX,centerY)[1])),radius,(0,0,255),1)
        
        for car in self.cars:
            carInStop = False
            for ls in self.allowedToGo:
                if car in ls:
                    carInStop = True
            # print(self.allowedToGo[id])
            if(self.distance(car.local_goal[0], car.local_goal[1], centerX,centerY) < STOP_SIGN_DIST and (not carInStop) and (not car in self.allowedToGo[id]) ):
                car.stopDrive()
                if not car in self.queue[id]:
                    self.queue[id].append(car)
                
        #let car go if no one is intersection 
        if len(self.queue[id]) > 0 :
            if(len(self.allowedToGo[id]) == 0):
                goCar = self.queue[id].pop(0)
                self.allowedToGo[id].append(goCar)
                # goCar.continue()
                goCar.continueDrive()
                
            
        #let car go if it can go
        # if len(self.allowedToGo[id]) > 0 and len(self.queue[id]) > 0:
        #     for i in range(min(2,len(self.queue[id]))):
        #         canGo = False
        #         # for j in range(len(self.allowedToGo[id])):
        #         #     # console.log(self.queue[id][i], self.allowedToGo[id][j])
        #         #     if(self.queue[id][i].pathCrosses(self.allowedToGo[id][j],3)):
        #         #         # //console.log("------------------------------------------------")
        #         #         canGo = False
                    
                    
                
        #     #    // console.log(canGo)
        #         if(canGo):
        #             goCar = self.queue[id].pop(0)
        #             self.allowedToGo[id].append(goCar)
        #             # goCar.continue()

        #             goCar.continueDrive()

                # //   console.log("can drive!!!!!!!!!!!!!!!! ",canGo)
                # //   console.log(goCar)
            #    // console.log("hello")
        
        self.allowedToGo[id] =  list(filter(lambda car: self.distance(car.local_goal[0], car.local_goal[1],centerX, centerY) < STOP_SIGN_DIST, self.allowedToGo[id]))
        # for car in self.cars:
        #     if self.distance(car.pos[0], car.pos[1],centerX, centerY) < STOP_SIGN_DIST:
        #         self.allowedToGo[id] = car