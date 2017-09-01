import cv2
import os
from datetime import datetime
from redis import Redis
import uuid


def main():
    #################### Setting up the connection ################
    subtype = 0 # 1: low res
    IP = os.environ.get('TARGET', 'ERROR_IP')
    EP = "rtsp://admin:admin@{0}:554/cam/realmonitor?channel=1&subtype={1}&unicast=true&proto=Onvif".format(IP, subtype)
    # test
    EP = "rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov"

    cap = cv2.VideoCapture(EP)
    ##################### Setting up parameters ################
    seconds = 0.25
    fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    multiplier = fps * seconds

    #################### Initiate Process ####################
    redis_conn = Redis(host='redis')
    print("Para {} fps, se tiene un multiplicador de {}".format(fps, multiplier))
    while cap.isOpened():
        frameId = int(round(cap.get(1)))
        ret, image = cap.read()

        if ret:
            if frameId % multiplier == 0:
                print('({})Processing...{}'.format(ret, frameId))
                # Save data about the frame
                array_dtype = str(image.dtype)
                l, w, k = image.shape
                # image = image.ravel().tostring()
                # # Generate a key
                # key = uuid.uuid4()
                # item = '{5}#{0}|{1}#{2}#{3}#{4}|{6}'.format(datetime.now(), array_dtype, l, w, k, IP, key)
                # # Push the data
                # redis_conn.set(key, image)
                # redis_conn.rpush('reconocer', item)
        else:
            break
    cap.release()
    # redis_conn.rpush('recolector_requests', "{}:{}".format('kill', os.environ.get('HOSTNAME')))


if __name__ == '__main__':
    main()
