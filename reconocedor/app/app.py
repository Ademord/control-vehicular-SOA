#!flask/bin/python
import subprocess
import numpy as np
import re
import cv2
import os
import requests
import json
import io


def reconocer(data=None):
    # create temp image
    path = "/usr/src/app/image.jpg"
    cv2.imwrite(path, data['frame'])
    del data['frame']
    # process image
    data['output'] = process_image(data, path)
    # format and send
    send(format_output(data))
    # delete temp image
    subprocess_execute(["rm", path])
    del data

def process_image(data, path):
    # use ALPR deamon to process
    args = ["alpr", path, "-c", "bo", "--config", "/usr/src/app/openalpr.conf", "-p","bo", "--clock"]
    try:
        return subprocess_execute(args)
        return format_output(data)
    except:
        abort(500)

def format_output(data):
    # process data received from daemon
    lines = []
    regex = re.compile(r'[\n\r\t]')
    for line in io.TextIOWrapper(data['output'].stdout, encoding="utf-8"):
        if not 'confidence' in line:
            continue
        line = regex.sub(' ', line)
        plate = re.findall('    - (.*?)  confidence', line, re.DOTALL)[0]
        confidence = re.findall('confidence: (.*?) ', line, re.DOTALL)[0]
        lines.append({"plate": plate, "confidence": confidence})

    mismatch = True
    if lines:
        first_plate = lines[0]
        data['plate'] = first_plate['plate']
        data['confidence'] = first_plate['confidence']
        # allowed range of mismatch
        pattern = re.compile(r"^\d{2,4}[A-Z]{2,3}$",re.I)
        if pattern.search(data['plate']):
            mismatch = False

    del data['output']
    data['mismatch'] = mismatch
    return data


def subprocess_execute(args):
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def send(data):
    url = os.environ.get('TARGET_SERVICE') + "/"
    headers = {'Content-Type': 'application/json'}
    if not data['mismatch']:
        # TODO save image
        r = requests.post(url.strip(), data=json.dumps(data), headers=headers)