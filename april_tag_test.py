from pupil_apriltags import Detector
import cv2
at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
while True:
        ret, frame_in = cap.read()
        grey = cv2.cvtColor(frame_in, cv2.COLOR_BGR2GRAY)
        tags = at_detector.detect(grey)
        for tag in tags:
            cv2.putText(frame_in, str(tag.tag_id), (int(tag.corners[1][0]),int(tag.corners[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3,cv2.LINE_AA)
            cv2.rectangle(frame_in, (int(tag.corners[0][0]),int(tag.corners[0][1])), (int(tag.corners[2][0]),int(tag.corners[2][1])), (255,0,0), 2)
        if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.imshow("camera", frame_in)