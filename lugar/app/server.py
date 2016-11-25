#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from app import Lugar as lugar
app = Flask(__name__)

@app.route('/lugares', methods=['GET'])
def index():
    lugares = lugar.getall()
    resultado = {}
    resultado['lugares'] = lugares
    return jsonify(resultado)

@app.route('/lugares/<int:id>', methods=['GET'])
def show(id):
    temp = lugar.get(id)
    if not temp: abort(404)
    resultado = {}
    resultado['lugar'] = temp
    return jsonify(resultado)

@app.route('/lugares', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not 'nombre' in request.json:
        abort(400)
    result = lugar.add(data)
    return jsonify({'result': result}), 201

@app.route('/lugares/<int:id>', methods=['PUT'])
def update(id):
    temp = lugar.get(id)
    data = request.get_json()
    if not temp or not data or not lugar.valid(data):
        abort(404)
    result = lugar.update(id, data)
    return jsonify({'result': result }), 201

@app.route('/lugares/<int:id>', methods=['DELETE'])
def destroy(id):
    temp = lugar.get(id)
    if not temp: abort(404)
    result = lugar.remove(id)
    return jsonify({'result': result }), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_first_request
def _run_on_start():
    lugar.connect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
    # app.run(port=55555, debug=True)
