#!flask/bin/python
from flask import Flask, jsonify
import requests
import json
import os
from datetime import datetime
app = Flask(__name__)

@app.route('/transmit', methods=['GET'])
def index():
    #build request to receiver
    data = {'timestamp': str(datetime.now())}
    url = os.environ.get('RECEIVER_IP', 'http://a6174ce25b32911e69b640206bb85836-1859478282.eu-central-1.elb.amazonaws.com') + "/receive"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url.strip(), data=json.dumps(data), headers=headers)
    return json.dumps(r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
