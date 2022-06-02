from translator import Translator
import cv2
from direction import Direction

from map import Map
from pupil_apriltags import Detector
from car_commands import *
class Camera:
    def __init__(self, corner_ids, car_ids, height, width, map, camId=0, goal_ids = []):
        self.map = map
        self.myMap = self.map.map
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.corner_ids = corner_ids
        self.car_ids = car_ids
        self.pos = {}
        self.dirs = {}
        self.goal_ids = goal_ids
        self.goals = {}
        self.goal_pos = {}
        for id in goal_ids:
            self.goals[id] = None
        for id in car_ids:
            self.pos[id] = None
            self.dirs[id] = 0
        self.at_detector =  Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
        self.tr = Translator(corner_ids[0], corner_ids[1], corner_ids[2],corner_ids[3], width,height, self.at_detector)
        ret, self.frame_in = self.cap.read()
    def update(self):
        ret, self.frame_in = self.cap.read()
        grey = cv2.cvtColor(self.frame_in, cv2.COLOR_BGR2GRAY)
        tags = self.at_detector.detect(grey)
        self.tr.setCoords(tags)
        if self.tr.foundCorners():
            sideLength_x = abs((self.tr.id2Coords[0]-40) - self.tr.id1Coords[0])
            sideLength_y = abs(self.tr.id4Coords[1] - self.tr.id1Coords[1])
            max_xi = len(self.myMap)
            max_yi = len(self.myMap[0])
            squareSide_x = sideLength_x/max_xi
            squareSide_y = sideLength_y/max_yi
            for i in range(max_xi):
                for j in range(max_yi):
                    # cv2.putText(self.frame_in, str((i,j)), (int(self.tr.inverse(i,j)[0]),int(self.tr.inverse(i,j)[1])), cv2.FONT_HERSHEY_SIMPLEX, .25 , (255,0,0), 1,cv2.LINE_AA)
                    # cv2.circle(self.frame_in, (int(self.tr.inverse(i,j)[0]),int(self.tr.inverse(i,j)[1])),5,(0,0,255),1)
                    # cv2.circle(self.frame_in, (int(self.tr.inverse(15,8)[0]),int(self.tr.inverse(8,4)[1])),30,(0,255,0),1)

                    #check if its a corner:
                    if (i == 0 and j == 0 
                        or i == 0 and j == max_yi
                        or i == max_xi and j == 0
                        or i == max_xi and j == max_yi):
                        continue
                    
                    if self.myMap[i][j].isRoad:
                        cell = self.myMap[i][j]
                        directions = cell.directions
                        
                        drawUpDown = len(directions) == 1 or (len(directions) == 2 and Direction.UP in directions and Direction.DOWN in directions)
                        drawLeftRight = len(directions) == 1 or (len(directions) == 2 and Direction.LEFT in directions and Direction.RIGHT in directions)
                        
                        if drawUpDown or drawLeftRight:
                            dir = directions[0]
                            #vertical line
                            # if dir == Direction.UP or dir == Direction.DOWN:
                                
                                # when dir == up: draw middle line, and when dir == left
                            
                            if dir == Direction.UP and Direction.RIGHT not in self.myMap[max(0, i-1)][j].directions or (dir == Direction.RIGHT and Direction.UP in self.myMap[i][max(0, j-1)].directions and len(self.myMap[i][max(0, j-1)].directions) == 1):
                                cv2.line(self.frame_in, 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2), int(self.tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2), int(self.tr.inverse(i,j)[1]) - int(2.0/4 * squareSide_y/2)), 
                                        (0,255,255), 1)
                                cv2.line(self.frame_in, 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2), int(self.tr.inverse(i,j)[1]) + int(2.0/4 * squareSide_y/2)), 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2), int(self.tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                        (0,255,255), 1)
                                #left side
                                # if dir == Direction.DOWN:
                                #     cv2.line(frame_in, 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                #             (0,0,0), 1)
                                # #right side
                                # if dir == Direction.UP:
                                #     cv2.line(frame_in, 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                #             (0,0,0), 1)
                                
                            #horizontal line   
                            # else:
                            if dir == Direction.LEFT and Direction.UP not in self.myMap[i][max(0, j-1)].directions or ((dir == Direction.UP and Direction.LEFT in self.myMap[min(max_xi-1, i+1)][j].directions and len(self.myMap[min(max_xi-1, i+1)][j].directions) == 1)):
                                cv2.line(self.frame_in, 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2), int(self.tr.inverse(i,j)[1] + squareSide_y/2)), 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2) + int(1.0/4 *squareSide_x), int(self.tr.inverse(i,j)[1] + squareSide_y/2)), 
                                        (0,255,255), 1)
                                cv2.line(self.frame_in, 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2) + int(3.0/4 * squareSide_x), int(self.tr.inverse(i,j)[1] + squareSide_y/2)), 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2 + squareSide_x), int(self.tr.inverse(i,j)[1] + squareSide_y/2)), 
                                        (0,255,255), 1)
                                # if dir == Direction.LEFT:
                                #     cv2.line(frame_in, 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                #             (0,0,0), 1)
                                # if dir == Direction.RIGHT:
                                #     cv2.line(frame_in, 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                #             (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                #             (0,0,0), 1)
                        # elif len(directions) == 2:
                        #     if Direction.UP in directions and Direction.LEFT in directions:
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1])), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2 + 1/2 * squareSide_x), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #     elif Direction.UP in directions and Direction.RIGHT in directions:
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2 + 1/2 * squareSide_x), int(tr.inverse(i,j)[1])), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2 + squareSide_x), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #     elif Direction.DOWN in directions and Direction.LEFT in directions:
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1])), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2 + 1/2 * squareSide_x), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #     elif Direction.DOWN in directions and Direction.RIGHT in directions:
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2 + 1/2 * squareSide_x), int(tr.inverse(i,j)[1])), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2 + squareSide_x), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                        #         cv2.line(frame_in, 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                        #                 (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x/2), int(tr.inverse(i,j)[1])), 
                        #                 (0,255,255), 1)
                    else:
                        cv2.rectangle(self.frame_in, 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2 ),int(self.tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x),int(self.tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                        (0,0,0), -1)
                        cv2.rectangle(self.frame_in, 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2 ),int(self.tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                        (int(self.tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x),int(self.tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                        (0,0,0), 1)

            cv2.rectangle(self.frame_in, 
                            (int(self.tr.inverse(0, 0)[0] - squareSide_x/2),int(self.tr.inverse(0,0)[1]) + int(squareSide_y/2)), 
                            (int(self.tr.inverse(max_xi, max_yi)[0] - squareSide_x/2),int(self.tr.inverse(max_xi, max_yi)[1]) + int(squareSide_y/2)), 
                            (0,0,0), 2)
                        

        # h = int(self.frame_in.shape[0]*1) # scale h
        # w = int(self.frame_in.shape[1]*1) # scale w
        # rsz_image = cv2.resize(self.frame_in, (w, h)) # resize image



        for tag in tags:
            if self.tr.foundCorners():
                if tag.tag_id in self.car_ids:
                    car = tag
                    self.pos[car.tag_id] = self.tr.translate(car.center[0], car.center[1], tags=tags)
                    pt1 = [(tag.corners[3][0]+tag.corners[0][0])/2, (tag.corners[3][1]+tag.corners[0][1])/2]
                    pt2 = [(tag.corners[1][0]+tag.corners[2][0])/2, (tag.corners[1][1]+tag.corners[2][1])/2]
                    current_vector = [pt1[0] - pt2[0], pt1[1] -pt2[1]]
                    # current_vector = self.tr.translate(current_vector[0], current_vector[1])

                    self.dirs[car.tag_id] = angle(current_vector[0], current_vector[1])
                elif tag.tag_id in self.goal_ids:
                    self.goals[tag.tag_id] = self.tr.translate(tag.center[0], tag.center[1])
            cv2.putText(self.frame_in, str(tag.tag_id), (int(tag.corners[1][0]),int(tag.corners[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3,cv2.LINE_AA)
            cv2.rectangle(self.frame_in, (int(tag.corners[0][0]),int(tag.corners[0][1])), (int(tag.corners[2][0]),int(tag.corners[2][1])), (255,0,0), 2)
    def get_pos(self, id):
        return self.pos[id]
    def get_goal_pos(self, id):
        return self.goals[id]
    def get_dir(self, id):
        return self.dirs[id] 
    def get_pos_dict(self):
        return self.pos

    def get_frame(self):
        return self.frame_in

    def get_goal(self, id):
        return self.goal_pos[id]

        
