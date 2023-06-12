from ultralytics import YOLO
from sort import SortTracker
import cv2
from detection_zone import DetectionZone
from video_loop import VideoLoop
from levels import Levels
import pafy


# Load a model
model = YOLO('yolov8n.pt')  # load an official detection modelpip
detection_zones = [DetectionZone(
    120, 300, 250, 350, Levels.ELEVATED)]


def overlap_event(zone1, zone2):
    print(f'{zone1} overlaps with {zone2}')


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=3T9F4JvtG4c"
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    vid_loop = VideoLoop(best.url)
    vid_loop.start(detection_zones, model, overlap_event)
