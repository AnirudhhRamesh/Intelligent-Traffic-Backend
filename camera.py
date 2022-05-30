from translator import Translator
import cv2
from pupil_apriltags import Detector
from car_commands import *
class Camera:
    def __init__(self, corner_ids, car_ids, height, width, camId=0, goal_ids = []):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.corner_ids = corner_ids
        self.car_ids = car_ids
        self.pos = {}
        self.dirs = {}
        self.goal_ids = goal_ids
        self.goals = {}
        self.goal_pos = {}
        for id in goal_ids:
            self.goals[id] = (0,0)
        for id in car_ids:
            self.pos[id] = (0,0)
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

        
