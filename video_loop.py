import cv2
from ultralytics import YOLO
from sort import SortTracker
from predicted_zone import PredictedZone
from typing import Any


class VideoLoop:
    def __init__(self, source: Any):
        self.__vid = cv2.VideoCapture(source)
        self.__tracker = SortTracker()

    def __frame_to_bytes(self, frame):
        ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def start(self, detection_zones: list, detection_cls_list: list, model: YOLO, overlap_callback: Any, draw_predicted: bool = True, draw_detection_zones: bool = True):
        while (True):
            _, frame = self.__vid.read()
            cv2.waitKey(1)
            prediction = model.predict(frame, verbose=False)[
                0].boxes.data.numpy()
            tracked = self.__tracker.update(prediction, _)
            for t in tracked:
                predicted = PredictedZone(x1=int(t[0]), y1=int(t[1]), x2=int(
                    t[2]), y2=int(t[3]), prob=float(t[4]), cls=int(t[5]), tracking_id=int(t[6]))
                if draw_predicted:
                    predicted.draw(frame)
                for zone in detection_zones:
                    if draw_detection_zones:
                        zone.draw(frame)

                    if zone.overlaps(predicted) and predicted.cls in detection_cls_list:
                        overlap_callback(zone, predicted)

            yield self.__frame_to_bytes(frame)
