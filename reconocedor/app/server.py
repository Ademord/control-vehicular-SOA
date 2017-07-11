#!flask/bin/python
from flask import Flask, abort, jsonify, request
from subprocess import check_output
import subprocess
app = Flask(__name__)
import numpy as np
import sys
import io
import re
import cv2
import os
import requests
import json
import functools


def compose(*functions):
	return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

URL = "/usr/src/app/image.jpg"
logs = [{
	"inicio": "mensaje inicial"	
}]

@app.route('/reconocer', methods=['POST'])
def _reconocer():
	logs.append({'reconocer':'hola'})
	# reconocer = compose(forward, clean, format, process, save)
	# results = forward(clean(format(process(save(request.get_json())))))
	return jsonify({'logs': logs})

# @app.route('/save', methods=['POST'])
def save(data):
	# logs.append({'save':'hola'})
	frame = np.array(data['frame'])
	cv2.imwrite(URL, frame); 
	#test image is saved
	# return jsonify({'logs': logs})
	return data

# @app.route('/process', methods=['GET'])
def process(data):
	# logs.append({'process':'hola'})
	# open frame with command line
	# test alpr works, by bashing into container first
	args = ["alpr", URL, "-c", "bo", "--config", "/usr/src/app/openalpr.conf", "-p","bo", "--clock"]
	try:
		data['output'] = subprocess.Popen(args, stdout=subprocess.PIPE)
		return data
	except:
		abort(500)

def format(data):
	# logs.append({'format':'hola'})
	lines = []
	regex = re.compile(r'[\n\r\t]')
	for line in io.TextIOWrapper(data['output'].stdout, encoding="utf-8"):
		if not 'confidence' in line:
			continue
		line = regex.sub(' ', line)
		plate = re.findall ( '    - (.*?)  confidence', line, re.DOTALL)[0]
		confidence = re.findall ( 'confidence: (.*?) ', line, re.DOTALL)[0]
		# logs.append({"plate found": line})
		lines.append({"plate": plate, "confidence": confidence})
	
	mismatch = True
	if lines:
		first_plate = lines[0]
		data['plate'] = first_plate['plate']
		data['confidence'] = first_plate['confidence']
	
		pattern = re.compile(r"^\d{2,4}[A-Z]{2,3}$",re.I)
		if pattern.search(data['plate']): 
			mismatch = False
	
	del data['output']
	data['mismatch'] = mismatch
	return data
	# return jsonify({'logs': logs[0]})

# @app.route('/delete', methods=['GET'])
def clean(data):
	# # destroy frame
	args = ["rm", URL]
	subprocess.Popen(args, stdout=subprocess.PIPE)
	# #test image is deleted
	# return jsonify("Deleted")
	return data

def forward(data):
	url = os.environ.get('TARGET_SERVICE') + "/"
	headers = {'Content-Type': 'application/json'}
	if not data['mismatch']:
		logs.append({'forward': 'sent to' + url})
		r = requests.post(url.strip(), data=json.dumps(data), headers=headers) 
	# else:
		# logs.append({'forward': 'NOT sent'})
	del data['frame']
	logs.append({'data': data})
	return data
	

@app.route('/', methods=['GET'])
def index():
	# logs.append({'hola': 'no he recibido nada'})
	return jsonify({'logs': logs})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
