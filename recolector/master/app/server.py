#!flask/bin/python
from flask import Flask, jsonify, make_response, request

import cv2
import numpy as np

import requests
import json
import os
from datetime import datetime

import subprocess

app = Flask(__name__)

config ={
    "ip": "123.123.111"    
}

@app.route('/', methods=['GET'])
def status():
    return jsonify(config)

@app.route('/<string:ip>', methods=['POST'])
def set_ip(ip):
    config['ip'] = ip
    return jsonify(config)


# def send(data):
#     data ['timestamp'] = str(datetime.now())
#     url = os.environ.get('TARGET_SERVICE') + "/reconocer"
#     headers = {'Content-Type': 'application/json'}
#     r = requests.post(url.strip(), data=json.dumps(data), headers=headers)
#     return jsonify({'result': 'sent to ' + url}), 201

# @app.route('/image', methods=['GET'])
# def readImage():
#     img = cv2.imread('image.jpg', 0)
#     return send({'ip': config['ip'], 'frame': img.tolist()})

@app.route('/video', methods=['GET'])
def readVideo():
    args = ['helm', 'install', os.environ['CHART_PATH']]
    subprocess.call(args)
    return jsonify({'result': 'process started'}), 201
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55551, debug=True)
