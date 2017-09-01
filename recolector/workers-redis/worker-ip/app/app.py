import cv2
import os
from datetime import datetime
from redis import Redis
import uuid
import time
import logging
from math import sqrt
import threading
import numpy as NP

# decorator to thread functions
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def Fibo(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

class RedisConnectError(BaseException): pass

class RecolectorIP():
    def __init__(self, container_name, redis_endpoint, camera_endpoint, redis_port=6379):
        self.redis_endpoint = redis_endpoint
        self.redis_port = redis_port
        self.camera_endpoint = camera_endpoint
        self.bind_redis()
        self.cap = None
        self.bind_camera()
        fps = self.cap.get(cv2.CAP_PROP_FPS)  # Gets the frames per second
        seconds = 0.25
        multiplier = fps * seconds
        logging.info("Para {} fps, se tiene un multiplicador de {}".format(fps, multiplier))
        self.image = None

    def bind_camera(self):
        self.cap = cv2.VideoCapture(self.camera_endpoint)

    def bind_redis(self):
        for retry_n in range(20):
            try:
                self.redis_client = Redis(host=self.redis_endpoint, port=self.redis_port)
                logging.info('Connected to Redis!')
            except:
                logging.info('Failed to connect to Redis. Retrying to connect in 15 seconds...')
                time.sleep(Fibo(retry_n))
                continue
            break
        else:
            raise RedisConnectError()

    def start(self):
        while self.cap.grab():
            self.ret, self.image = self.cap.retrieve()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        # redis_conn.rpush('recolector_requests', "{}:{}".format('kill', os.environ.get('HOSTNAME')))

    def pack_data(self, key):
        # Save data about the frame
        array_dtype = str(self.image.dtype)
        l, w, k = (list(self.image.shape) + [None] * 3)[:3]
        item = '{5}#{0}|{1}#{2}#{3}#{4}|{6}'.format(datetime.now(), array_dtype, l, w, k, '', key)
        image = NP.fromstring(self.image, dtype=array_dtype).reshape(int(l), int(w), int(k))
        logging.info(item)
        return item

    @threaded
    def start_pusher(self):
        while True:
            if self.image != None:
                key = str(uuid.uuid4())[:8]
                path = '/app/media/' + key + '.png' # OPTIONAL
                cv2.imwrite(path, self.image) # OPTIONAL
                item = self.pack_data(key)
                string_image = self.image.ravel().tostring()
                self.redis_client.set(key, string_image)
                self.redis_client.rpush('reconocer', item)
            time.sleep(3)

def main():
    logging.getLogger().setLevel(logging.INFO)
    redis_endpoint = os.environ.get('REDIS_SERVICE_HOST', '192.168.99.100')
    redis_port = 31896
    container_name = os.environ.get('HOSTNAME')
    #################### Setting up the connection ################
    subtype = 0  # 1: low res
    IP = os.environ.get('TARGET', '190.186.38.110')
    # DAHUA
    # camera_endpoint = "rtsp://admin:admin@{0}:554/cam/realmonitor?channel=1&subtype={1}&unicast=true&proto=Onvif".format(IP, subtype)
    # VIVOTEK

    camera_endpoint = "rtsp://{0}:554/live.sdp:".format(IP)
    # camera_endpoint = "rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov"
    camera_endpoint = 0
    logging.info('{}'.format(camera_endpoint))
    with RecolectorIP(container_name=container_name,
                      redis_endpoint=redis_endpoint,
                      redis_port=redis_port,
                      camera_endpoint=camera_endpoint) as recolector:
        recolector.start_pusher()
        recolector.start()

if __name__ == '__main__':
    main()
