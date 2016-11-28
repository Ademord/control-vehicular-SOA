#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from app import Propietario
app = Flask(__name__)

@app.route('/propietarios', methods=['GET'])
def index():
    temp = Propietario.getall()
    resultado = {}
    resultado['propietarios'] = temp
    return jsonify(resultado)

@app.route('/propietarios/<int:id>', methods=['GET'])
def show(id):
    temp = Propietario.get(id)
    if not temp: abort(404)
    resultado = {}
    resultado['propietario'] = temp
    return jsonify(resultado)

@app.route('/propietarios', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not Propietario.valid(data):
        abort(400)
    result = Propietario.add(data)
    return jsonify({'result': result}), 201

@app.route('/propietarios/<int:id>', methods=['PUT'])
def update(id):
    temp = Propietario.get(id)
    data = request.get_json()
    if not temp or not data or not Propietario.valid(data):
        abort(404)
    result = Propietario.update(id, data)
    return jsonify({'result': result }), 201

@app.route('/propietarios/<int:id>', methods=['DELETE'])
def destroy(id):
    temp = Propietario.get(id)
    if not temp: abort(404)
    result = Propietario.remove(id)
    return jsonify({'result': result }), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_first_request
def _run_on_start():
    Propietario.connect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
    # app.run(port=55555, debug=True)
