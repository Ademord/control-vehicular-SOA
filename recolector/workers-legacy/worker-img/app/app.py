import cv2
import os
from datetime import datetime
import requests
import json


def send(data):
    data['timestamp'] = str(datetime.now())
    url = os.environ.get('TARGET_SERVICE') + "/reconocer"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url.strip(), data=json.dumps(data), headers=headers)


def main():
    print(os.environ.get('TARGET_SERVICE', 'http://reconocedor'))
    print(os.environ.get('TARGET'))

    # IMAGE RECOGNITION
    frame = cv2.imread(os.environ.get('TARGET'), 0)
    send({'ip': 'unset', 'frame': frame.tolist()})

if __name__ == '__main__':
    main()
