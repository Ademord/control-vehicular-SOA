#!/usr/bin/env python
import rediswq
from redis import Redis
import subprocess
import numpy as NP
import re
import cv2
import os
import requests
import json
import io
import logging
from math import sqrt
import time
from datetime import datetime

class Reconocedor():
    def __init__(self, ip, timestamp, image):
        self.path = "/usr/src/app/image.jpg"
        self.data = {
            'ip': ip or 'unset',
            'timestamp': timestamp,
            'frame': image,
            'plate': None,
            'confidence': None,
            'mismatch': None
        }

    def subprocess_execute(self, args):
        return subprocess.Popen(args, stdout=subprocess.PIPE)

    def process(self):
        cv2.imwrite(self.path, self.data['frame'])
        # del data['frame']
        command = ["alpr", self.path, "-c", "bo", "--config", "/usr/src/app/openalpr.conf", "-p", "bo", "--clock"]
        output = self.subprocess_execute(command).stdout
        lines = self.parse(output)
        if len(lines) > 0:
            self.data['plate'] = lines[0]['plate']
            self.data['confidence'] = lines[0]['confidence']
            self.data['mismatch'] = self.get_mismatch(self.data['plate'])
            self.subprocess_execute(["rm", self.path])
            return True
        else:
            logging.info("No data found in output")
            return False

    def parse(self, output):
        # process data received from daemon
        lines = []
        regex = re.compile(r'[\n\r\t]')
        for line in io.TextIOWrapper(output, encoding="utf-8"):
            if not 'confidence' in line:
                continue
            line = regex.sub(' ', line)
            plate = re.findall(r'    - (.*?)  confidence', line, re.DOTALL)[0]
            confidence = re.findall(r'confidence: (.*?) ', line, re.DOTALL)[0]
            lines.append({'plate': plate, 'confidence': confidence})
        return lines

    def get_mismatch(self, plate):
        # allowed range of mismatch
        mismatch = True
        pattern = re.compile(r'^\d{2,4}[A-Z]{2,3}$', re.I)
        if pattern.search(plate):
            mismatch = False
        return mismatch

    def pack_data(self, key):
        # Save data about the frame
        array_dtype = str(self.data['frame'].dtype)
        l, w, k = (list(self.data['frame'].shape) + [None] * 3)[:3]
        item = '{5}#{0}|{1}#{2}#{3}#{4}|{6}'.format(self.data['timestamp'], array_dtype, l, w, k, self.data['ip'], key)
        self.data['item'] = item
        del self.data['frame']
        return self.data

def Fibo(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

class RedisConnectError(BaseException): pass

class FramesWorker():
    def __init__(self, redis_endpoint):
        self.redis_endpoint = redis_endpoint
        self.q = None
        self.key = None
        self.item = None
        self.bind_redis()

    def bind_redis(self):
        for retry_n in range(20):
            try:
                self.redis_client = Redis(host=self.redis_endpoint)
                self.q = rediswq.RedisWQ(name="reconocer", host=self.redis_endpoint)
                logging.info('Connected to Redis!')
            except:
                logging.info('Failed to connect to Redis. Retrying to connect in 15 seconds...')
                time.sleep(Fibo(retry_n))
                continue
            break
        else:
            raise RedisConnectError()

    def decode_frame(self, item, key):
        array_dtype, l, w, k = item.split('|')[1].split('#')
        image = self.redis_client.get(key)
        image = NP.fromstring(image, dtype=array_dtype).reshape(int(l), int(w), int(k))
        return image

    def send(self, data):
        url = os.environ.get('TARGET_SERVICE') + "/"
        headers = {'Content-Type': 'application/json'}
        if not data['mismatch']:
            captured_date = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            elapsed_time = datetime.now() - captured_date
            logging.info('Sending data - processing took {} seconds'.format(elapsed_time.seconds))
            r = requests.post(url.strip(), data=json.dumps(data), headers=headers)

    def unpack_bytes(self, item):
        # item: $IP#$TIMESTAMP|$FRAME_DIMENSIONS|$FRAME_REDIS_KEY
        # $FRAME_DIMENSIONS: uint8#720#1280#3
        key = item.split('|')[2]
        image = self.decode_frame(item, key)
        ip, timestamp = item.split('|')[0].split('#')
        return key, image, ip, timestamp

    def serve(self):
        logging.info("Worker with sessionID: " + self.q.sessionID())
        logging.info("Initial queue state: empty=" + str(self.q.empty()))

        while True:
            # time.sleep(10)
            if not self.q.empty():
                item = self.q.lease(lease_secs=10, block=True, timeout=2)
                if item is not None:
                    key, image, ip, timestamp = self.unpack_bytes(item.decode('utf-8'))
                    reconocedor = Reconocedor(ip, timestamp, image)

                    if reconocedor.process():
                        self.send(reconocedor.pack_data(key))
                    else:
                        self.redis_client.delete(key)
                    self.q.complete(item)
            # else: logging.info("Waiting for work")

def main():
    logging.getLogger().setLevel(logging.INFO)
    redis_endpoint = os.environ.get('REDIS_SERVICE_HOST', 'redis')
    container_name = os.environ.get('HOSTNAME')
    FramesWorker(redis_endpoint=redis_endpoint).serve()

if __name__ == '__main__':
    main()