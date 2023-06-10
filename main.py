from ultralytics import YOLO
from sort import SortTracker
import cv2
import numpy as np
import pafy
from zone import Zone, create_zone_from_arr


# Load a model
model = YOLO('yolov8n.pt')  # load an official detection modelpip
vid = cv2.VideoCapture(0)
tracker = SortTracker()
detection_zone = Zone(10, 10, 100, 650)

def start_video_loop(): 
      while(True):
         _, frame = vid.read()
         cv2.waitKey(1)

         prediction = model.predict(frame)[0].boxes.data.numpy()
         
         tracked = tracker.update(prediction, _)
         human_in_zone_arr = []
         for t in tracked:
            z = create_zone_from_arr(t)
            z.draw(frame)
            detection_zone.draw(frame)
            human_in_zone_arr.append(detection_zone.overlaps(z) and z.cls == 0)
            
         if any(human_in_zone_arr):  
               cv2.putText(frame, "HUMAN INSIDE ZONE", (50, 50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,color=(0, 0, 250))
         else:
            cv2.putText(frame, "ZONE CLEAR", (50, 50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,color=(250, 0, 0))

         cv2.imshow("window", frame)
if __name__ == "__main__":
    start_video_loop()
   