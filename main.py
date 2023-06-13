from flask import Flask
from ultralytics import YOLO
from sort import SortTracker
import cv2
from detection_zone import DetectionZone
from video_loop import VideoLoop
from levels import Levels
import pafy

from flask import Flask, render_template, Response, request


app = Flask(__name__)


# Load a model
model = YOLO('yolov8n.pt')  # load an official detection modelpip
detection_zones = [DetectionZone(
    0, 0, 350, 350, Levels.ELEVATED)]

detection_cls_list = [0] #Human only

def overlap_event(zone1, zone2):
    print(f'{zone1} overlaps with {zone2}')


@app.route('/')
def index():
    url = "https://www.youtube.com/watch?v=It5EQwYLQB8"
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    vid_loop = VideoLoop(best.url)
    return Response(vid_loop.start(detection_zones, detection_cls_list, model, overlap_event, False, False), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run()