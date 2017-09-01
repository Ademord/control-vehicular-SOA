import cv2
import os
from datetime import datetime
import requests
import json
from flask import jsonify
from random import randint

def send(data):
    data ['timestamp'] = str(datetime.now())
    url = os.environ.get('TARGET_SERVICE', 'http://reconocedor') + "/reconocer"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url.strip(), data=json.dumps(data), headers=headers)

def main():
    print(os.environ.get('TARGET_SERVICE', 'http://reconocedor'))
    print(os.environ.get('TARGET'))

    # VIDEO RECOGNITION FROM CAMERA
    # TODO ADJUST WITH CODE FROM worker-vid
    cap = cv2.VideoCapture(os.environ.get('VIDEO_NAME', 'video1.avi'))
    seconds = 0.15
    fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    multiplier = fps * seconds
    print("Para {} fps, se tiene un multiplicador de {}".format(fps, multiplier))
    while(cap.isOpened()):
        frameId = int(round(cap.get(1)))
        ret, frame = cap.read()

        if ret:
            if frameId % multiplier == 0:
                print('({})Processing...{}'.format(ret, frameId))
                # print(frame)
                send({'ip': os.environ.get('IP', '123.123.111'), 'frame': frame.tolist()})
        else:
            break
    cap.release()

if __name__ == '__main__':
    main()
