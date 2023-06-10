import cv2
from ultralytics import YOLO
from sort import SortTracker
from predicted_zone import PredictedZone
from typing import Any


class VideoLoop:
    def __init__(self, source: Any):
        self.__vid = cv2.VideoCapture(source)
        self.__tracker = SortTracker()

    def start(self, detection_zones: list, model: YOLO, overlap_callback: Any):
        while (True):
            _, frame = self.__vid.read()
            cv2.waitKey(1)

            prediction = model.predict(frame, verbose=False)[0].boxes.data.numpy()

            tracked = self.__tracker.update(prediction, _)
            human_in_zone_arr = []
            for t in tracked:

                z = PredictedZone(x1=int(t[0]), y1=int(t[1]), x2=int(t[2]), y2=int(t[3]), prob=float(t[4]), cls=int(t[5]))
                z.draw(frame)
                for d in detection_zones:
                    d.draw(frame)
                    if d.overlaps(z):
                        overlap_callback(d, z)
                    human_in_zone_arr.append(d.overlaps(z) and z.cls == 0)

            if any(human_in_zone_arr):
                cv2.putText(frame, "HUMAN INSIDE ZONE", (50, 50),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 0, 250))
            else:
                cv2.putText(frame, "ZONE CLEAR", (50, 50),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(250, 0, 0))

            cv2.imshow("window", frame)
