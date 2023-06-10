from typing import Any
import cv2
from abstract_zone import AbstractZone
    
class PredictedZone(AbstractZone):
    def __init__(self, x1:int, y1:int, x2:int, y2:int, prob:float, cls:int, tracking_id:int=None) -> None:
        super().__init__(x1,y1,x2,y2)
        self.prob = prob
        self.cls = cls
        self.tracking_id = tracking_id
