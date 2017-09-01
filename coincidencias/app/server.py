#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, send_from_directory
from app import Coincidencia
import os

app = Flask(__name__)
logs = [{
    "inicial":"init"
}
]
@app.route('/', methods=['GET'])
def index():
    return jsonify(Coincidencia.getall())

@app.route('/<int:id>', methods=['GET'])
def show(id):
     return jsonify(Coincidencia.get(id))

@app.route('/search/<string:q>', methods=['GET'])
def search(q):
    return jsonify(Coincidencia.buscar(q))

@app.route('/query', methods=['POST'])
def raw():
    q = request.get_json()
    Coincidencia.raw(q['query'])
    return "Added", 200

@app.route('/count/lugar', methods=['GET'])
def getCountByPlace():
    return jsonify(Coincidencia.getCountByPlace())

@app.route('/date-count/propietarios', methods=['GET'])
def getDateCountKnown():
    return jsonify(Coincidencia.getDateCountKnown())

@app.route('/date-count/desconocidos', methods=['GET'])
def getDateCountUnknown():
    return jsonify(Coincidencia.getDateCountUnknown())

@app.route('/count/propietarios', methods=['GET'])
def getCountKnown():
    return jsonify(Coincidencia.getCountKnown())

@app.route('/count/desconocidos', methods=['GET'])
def getCountUnknown():
    return jsonify(Coincidencia.getCountUnknown())

@app.route('/count/propietarios/lugar', methods=['GET'])
def getCountKnownByPlace():
    return jsonify(Coincidencia.getCountKnownByPlace())

@app.route('/count/desconocidos/lugar', methods=['GET'])
def getCountUnknownByPlace():
    return jsonify(Coincidencia.getCountUnknownByPlace())

@app.route('/', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not Coincidencia.valid(data):
        abort(400)
    return jsonify(Coincidencia.add(data)), 201

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.environ.get('UPLOADS_PATH', '/usr/src/data/')
    return send_from_directory(directory=uploads, filename=filename)

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
