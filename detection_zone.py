from typing import Any
import cv2
from abstract_zone import AbstractZone
from levels import Levels
    
class DetectionZone(AbstractZone):
    def __init__(self, x1:int, y1:int, x2:int, y2:int, level:Levels) -> None:
        super().__init__(x1,y1,x2,y2)
        self.level = level
    
    def __repr__(self) -> str:
        return f"DetectionZone: LEVEL: {self.level}"
