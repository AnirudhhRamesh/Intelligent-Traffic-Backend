class Translator:
    #coords are numbered anti-clockwise from the bottom left
    def __init__(self, id1, id2, id3, id4, x_size, y_size, atd, tag_size=0.05, camera_params=[2.21589934e+03, 1.32500546e+03, 2.27352325e+03, 6.64867852e+02], tags = None):
        self.id1 = id1
        self.id1Coords = None
        self.id2 = id2
        self.id2Coords = None
        self.id3 = id3
        self.id3Coords = None
        self.id4 = id4 
        self.id4Coords = None
        self.x = x_size
        self.y = y_size
        self.atd = atd
        self.tag_size = tag_size
        self.cam_param = camera_params
        self.setCoords(tags)
        
    def setCoords(self, tags):
        if not (tags is None):
            # grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # #todo: make modular for camera
            # tags = self.atd.detect(grey, estimate_tag_pose=False, camera_params = self.cam_param, tag_size = self.tag_size)
            # print(tags)
            for tag in tags:
                if tag.tag_id == self.id1:
                    self.id1Coords = tag.center
                elif tag.tag_id == self.id2:
                    self.id2Coords = tag.center
                    # self.id2Coords[0] = self.id2Coords[0] - 40
                elif tag.tag_id == self.id3:
                    self.id3Coords = tag.center
                elif tag.tag_id == self.id4:
                    self.id4Coords = tag.center
    def translate(self,x,y,tags=None):
        self.setCoords(tags)
        if self.foundCorners():
            nx = (x - self.id1Coords[0]) / abs((self.id2Coords[0]-40) - self.id1Coords[0]) * self.x - 1
            ny = (y - self.id1Coords[1]) / (-1*abs(self.id4Coords[1] - self.id1Coords[1])) * self.y
            return (nx, ny)
        return None
    def inverse(self,x,y,tags=None):
        self.setCoords(tags)
        if self.foundCorners():
            px = (x+1) / self.x * abs((self.id2Coords[0]-40) - self.id1Coords[0]) + self.id1Coords[0]
            py = y / self.y * -abs(self.id4Coords[1] - self.id1Coords[1]) + self.id1Coords[1]
            return(px,py)
        return None
    def foundCorners(self, tags = None):
        self.setCoords(tags)
        return not (self.id1Coords is None) and not (self.id2Coords is None) and not (self.id4Coords is None)

