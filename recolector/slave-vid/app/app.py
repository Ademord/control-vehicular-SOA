import cv2
import os
from datetime import datetime
import json
from flask import jsonify
import grequests
import numpy as np
import time
tic = time.clock()
   
def main():
    print(os.environ.get('TARGET_SERVICE', 'http://reconocedor'))
    print(os.environ.get('VIDEO_NAME', 'video1.avi'))
    print(os.environ.get('IP', '123.123.111'))

    # IMAGE RECOGNITION
    # frame = cv2.imread('image.jpg', 0)
    # send({'ip': os.environ.get('IP', '123.123.111'), 'frame': frame.tolist()})

    # VIDEO RECOGNITION 
    #################### Setting up the file ################
    vidcap = cv2.VideoCapture(os.environ.get('VIDEO_NAME', 'video1.avi'))
    success, frame = vidcap.read()
    # #################### Setting up parameters ################
    #OpenCV is notorious for not being able to good to 
    # predict how many frames are in a video. The point here is just to 
    # populate the "desired_frames" list for all the individual frames
    # you'd like to capture. 

    est_tot_frames  = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('cuadros totales', est_tot_frames)

    n = 30                            # Desired interval of frames to include
    desired_frames = np.arange(1, est_tot_frames, n) 
    #################### Initiate Process ################
    rs = []
    responses_list = []
    print('cuadros deseados', len(desired_frames), ": " , desired_frames)
    for i in desired_frames:
        vidcap.set(1,i-1)                      
        success, image = vidcap.read(1)         # image is an array of array of [R,G,B] values
        if success: 
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                'ip': os.environ.get('IP', '123.123.111'), 
                'frame': image.tolist(),
                'timestamp': str(datetime.now())
            }
            url = os.environ.get('TARGET_SERVICE', 'http://reconocedor') + "/reconocer"
            rs.append(grequests.post(url.strip(), data=json.dumps(data), headers=headers))
        # if (i-1)%(n*10) == 0:
        #     print("llamada", i)
        #     responses_list = grequests.map(rs)
        #     rs = []
            
        # print('Sending frame #', i)
    responses_list = grequests.map(rs)
    vidcap.release()
    toc = time.clock()
    print("Complete ", toc - tic, " : ", responses_list)

if  __name__ =='__main__':
    main()
