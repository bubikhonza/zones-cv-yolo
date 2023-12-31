import cv2
from typing import Any


class AbstractZone:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rect = x1, y1, x2, y2

    def overlaps(self, other: 'AbstractZone') -> bool:
        # TODO: solve overlapping without corners
        pt1 = other.x1, other.y1
        pt2 = other.x1, other.y2
        pt3 = other.x2, other.y1
        pt4 = other.x2, other.y2
        cond1 = self.rect[0] < pt1[0] < self.rect[0] + \
            self.rect[2] and self.rect[1] < pt1[1] < self.rect[1]+self.rect[3]
        cond2 = self.rect[0] < pt2[0] < self.rect[0] + \
            self.rect[2] and self.rect[1] < pt2[1] < self.rect[1]+self.rect[3]
        cond3 = self.rect[0] < pt3[0] < self.rect[0] + \
            self.rect[2] and self.rect[1] < pt3[1] < self.rect[1]+self.rect[3]
        cond4 = self.rect[0] < pt4[0] < self.rect[0] + \
            self.rect[2] and self.rect[1] < pt4[1] < self.rect[1]+self.rect[3]
        return cond1 or cond2 or cond3 or cond4

    def draw(self, frame: Any) -> None:
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2),
                      color=(255, 255, 0), thickness=2)
