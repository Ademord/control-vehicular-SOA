import cv2
import os
from datetime import datetime
import requests
import json
from flask import jsonify
import server
from random import randint

def send(data):
	data ['timestamp'] = str(datetime.now())
	url = os.environ.get('TARGET_SERVICE') + "/reconocer"
	headers = {'Content-Type': 'application/json'}
	r = requests.post(url.strip(), data=json.dumps(data), headers=headers)

def main():
	config = server.config
	aleatorio = randint(1,3)
	# cap = cv2.VideoCapture('video{}.avi'.format(aleatorio))
	cap = cv2.VideoCapture('video1.avi')

	seconds = 0.15
	fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
	multiplier = fps * seconds
	
	while(cap.isOpened()):
		frameId = int(round(cap.get(1)))
		ret, frame = cap.read()
		
		if ret and frameId % multiplier == 0:
			send({'ip': '123.123.111', 'frame': frame.tolist()})
	
	cap.release()

if  __name__ =='__main__':
	main()
