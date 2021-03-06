import sys as Sys
from ctypes.wintypes import tagSIZE
from threading import Thread

from pupil_apriltags import Detector

from direction import Direction

Sys.path.append("..")
import os as Os
import time as Time
import urllib.request
from queue import Queue

import cv2
import numpy as np
from imutils.video import videostream
from map import Map

from translator import Translator


class FileVideoStream:
    def __init__(self, mapFile):#, path, queueSize=128):
        # self.stream = videostream.VideoStream(path, framerate=32).start()
        # self.stopped = True
        # self.frame = self.stream.read()
        self.map = Map(mapFile)
        self.myMap = self.map.map
        
        self.startStream()
    def start(self):
        self.stopped = False
        t = Thread(target=self.update, args=())
        # t.daemon = true_divide
        t.start()
        return self
    def update(self):
        while True:
            if self.stopped:
                return
            # req = urllib.request.urlopen('http://128.179.154.82:8080/video')
            # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            # frame_in = cv2.imdecode(arr, -1) # 'Load it as it is'
            self.frame = self.stream.read()
    def read(self):
        return self.frame
    def more(self):
        return True
    def stop(self):
        self.stopped = True

    def foreach(ls, fn):
        for i in range(len(ls)):
            ls[i] = fn(ls[i])

    # fvs = FileVideoStream('http://192.168.137.79:8080/video').start()
    #os.add_dll_directory("C:\\Users\\LucaS\\MIT\\GitHub\\apriltags\\src\\pupil_apriltags\\lib\\apriltag.dll")

    def startStream(self):
        print("start!\n")

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
        # cap =  videostream.VideoStream(src='http://192.168.137.79:8080/video', framerate=24, resolution=(1920,1260)).start()
        Time.sleep(1)
        at_detector = Detector(families='tag36h11',
                            nthreads=1,
                            quad_decimate=1.0,
                            quad_sigma=0.0,
                            refine_edges=1,
                            decode_sharpening=0.25,
                            debug=0)


        print("starting stream!")
        corner_ids = [4,18,0,6]# [4,18,0,6]
        tr = Translator(corner_ids[0], corner_ids[1], corner_ids[2],corner_ids[3], self.map.max_x, self.map.max_y,at_detector)

        #map2d = Map.parseFile("map.txt")

        while True:
            ret, frame_in = cap.read()
            # frame_in = fvs.read() #.read()
            # frame_in = cap.read()
            # req = urllib.request.urlopen('http://192.168.11.88/capture')
            # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            # frame_in = cv2.imdecode(arr, -1) # 'Load it as it is'
            
            grey = cv2.cvtColor(frame_in, cv2.COLOR_BGR2GRAY)
            
            
        # [[2.21589934e+03 0.00000000e+00 1.32500546e+03]
        #  [0.00000000e+00 2.27352325e+03 6.64867852e+02]
        #  [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
            tags = at_detector.detect(grey, estimate_tag_pose=True, camera_params = [2.21589934e+03, 1.32500546e+03, 2.27352325e+03, 6.64867852e+02], tag_size = 0.05)
            if(len(tags) > 0):
                tr.setCoords(tags)
                # print(tags[0])
                for i in range(len(tags)):
                    # if tags[i].tag_id == 0:
                    #cv2.putText(frame_in, str(tags[i].pose_t), [20,40], cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1,cv2.LINE_AA)
                    cv2.putText(frame_in, str(tags[i].tag_id), (int(tags[i].corners[1][0]),int(tags[i].corners[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3,cv2.LINE_AA)
                    cv2.rectangle(frame_in, (int(tags[i].corners[0][0] ),int(tags[i].corners[0][1])), (int(tags[i].corners[2][0]),int(tags[i].corners[2][1])), (255,0,0), 2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if tr.foundCorners():
                
                sideLength_x = abs(tr.id2Coords[0] - tr.id1Coords[0])
                sideLength_y = abs(tr.id4Coords[1] - tr.id1Coords[1])
                max_xi = len(self.myMap)
                max_yi = len(self.myMap[0])
                squareSide_x = sideLength_x/max_xi
                squareSide_y = sideLength_y/max_yi
                for i in range(max_xi):
                    for j in range(max_yi):
                        # cv2.putText(frame_in, str((i,j)), (int(tr.inverse(i,j)[0]),int(tr.inverse(i,j)[1])), cv2.FONT_HERSHEY_SIMPLEX, .25 , (255,0,0), 1,cv2.LINE_AA)
                        # cv2.circle(frame_in, (int(tr.inverse(i,j)[0]),int(tr.inverse(i,j)[1])),5,(0,0,255),1)
                        # cv2.circle(frame_in, (int(tr.inverse(8,4)[0]),int(tr.inverse(8,4)[1])),30,(0,255,0),1)

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
                                    cv2.line(frame_in, 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) - int(2.0/4 * squareSide_y/2)), 
                                            (0,255,255), 1)
                                    cv2.line(frame_in, 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) + int(2.0/4 * squareSide_y/2)), 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
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
                                    cv2.line(frame_in, 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2), int(tr.inverse(i,j)[1] + squareSide_y/2)), 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(1.0/4 *squareSide_x), int(tr.inverse(i,j)[1] + squareSide_y/2)), 
                                            (0,255,255), 1)
                                    cv2.line(frame_in, 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(3.0/4 * squareSide_x), int(tr.inverse(i,j)[1] + squareSide_y/2)), 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2 + squareSide_x), int(tr.inverse(i,j)[1] + squareSide_y/2)), 
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
                            cv2.rectangle(frame_in, 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2 ),int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x),int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                            (0,0,0), -1)
                            cv2.rectangle(frame_in, 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2 ),int(tr.inverse(i,j)[1]) - int(squareSide_y/2)), 
                                            (int(tr.inverse(i,j)[0] - squareSide_x/2) + int(squareSide_x),int(tr.inverse(i,j)[1]) + int(squareSide_y/2)), 
                                            (0,0,0), 1)

                cv2.rectangle(frame_in, 
                              (int(tr.inverse(0, 0)[0] - squareSide_x/2),int(tr.inverse(0,0)[1]) + int(squareSide_y/2)), 
                              (int(tr.inverse(max_xi, max_yi)[0] - squareSide_x/2),int(tr.inverse(max_xi, max_yi)[1]) + int(squareSide_y/2)), 
                              (0,0,0), 2)
                            



            h = int(frame_in.shape[0]*1) # scale h
            w = int(frame_in.shape[1]*1) # scale w
            rsz_image = cv2.resize(frame_in, (w, h)) # resize image


            cv2.imshow('camera', frame_in)

            cv2.resizeWindow('camera', w, h) # resize window

        # cap.release()
        cv2.destroyAllWindows()



print(1/2, 1.0/2, 1.0/2.0)
myStream = FileVideoStream("map3.csv")