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
