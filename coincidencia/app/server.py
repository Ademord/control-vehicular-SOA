#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from app import Coincidencia
import cv2
import numpy as np
import json
import requests
app = Flask(__name__)
logs = [{
    "inicial":"init"
}
]

def get_external(url):
    r = requests.get(url.strip())
    return r.json()

@app.route('/', methods=['GET'])
def index():
    data = get_external('http://lugares/')
    # temp = Coincidencia.getall()
    # resultado = {}
    # resultado['coincidencias'] = temp
    return jsonify({"logs": data})

@app.route('/<int:id>', methods=['GET'])
def show(id):
    temp = Coincidencia.get(id)
    if not temp: abort(404)
    resultado = {}
    resultado['coincidencia'] = temp
    return jsonify(resultado)

@app.route('/', methods=['POST'])
def store():
    data = request.get_json()
    cv2.imwrite('/usr/src/data/image.jpg', np.array(data['frame'])); 
    del data['frame']
    logs.append(data)
    if not request.json or not Coincidencia.valid(data):
        abort(400)
    # PREPARE DATA
    coincidencia.camara = temp['ip']

    # coincidencia.lugar = temp['lugar']
    # coincidencia.miembro = temp['miembro']
    # coincidencia.filename = temp['filename']
    coincidencia.placa = temp['plate']
    # coincidencia.mime = temp['mime']
    # coincidencia.mismatch = temp['mismatch']
    # STORE DATA
    # result = Coincidencia.add(data)
    return jsonify({'logs': logs}), 201

@app.route('/<int:id>', methods=['PUT'])
def update(id):
    temp = Coincidencia.get(id)
    data = request.get_json()
    if not temp or not data or not Coincidencia.valid(data):
        abort(404)
    result = Coincidencia.update(id, data)
    return jsonify({'result': result }), 201

@app.route('/<int:id>', methods=['DELETE'])
def destroy(id):
    temp = Coincidencia.get(id)
    if not temp: abort(404)
    result = Coincidencia.remove(id)
    return jsonify({'result': result }), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_first_request
def _run_on_start():
    Coincidencia.connect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
    # app.run(port=55555, debug=True)
