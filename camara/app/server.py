#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from app import Camara
app = Flask(__name__)

@app.route('/camaras', methods=['GET'])
def index():
    temp = Camara.getall()
    resultado = {}
    resultado['camaras'] = temp
    return jsonify(resultado)

@app.route('/camaras/<int:id>', methods=['GET'])
def show(id):
    temp = Camara.get(id)
    if not temp: abort(404)
    resultado = {}
    resultado['camara'] = temp
    return jsonify(resultado)

@app.route('/camaras', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not Camara.valid(data):
        abort(400)
    result = Camara.add(data)
    return jsonify({'result': result}), 201

@app.route('/camaras/<int:id>', methods=['PUT'])
def update(id):
    temp = Camara.get(id)
    data = request.get_json()
    if not temp or not data or not Camara.valid(data):
        abort(404)
    result = Camara.update(id, data)
    return jsonify({'result': result }), 201

@app.route('/camaras/<int:id>', methods=['DELETE'])
def destroy(id):
    temp = Camara.get(id)
    if not temp: abort(404)
    result = Camara.remove(id)
    return jsonify({'result': result }), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_first_request
def _run_on_start():
    Camara.connect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55551, debug=True)
    # app.run(port=55555, debug=True)
