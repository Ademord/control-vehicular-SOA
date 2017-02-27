#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from app import Matricula
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify(Matricula.getall())

@app.route('/<int:id>', methods=['GET'])
def show(id):
     return jsonify(Matricula.get(id))

@app.route('/search/<string:q>', methods=['GET'])
def search(q):
    return jsonify(Matricula.buscar(q))

@app.route('/propietario/<int:id>', methods=['GET'])
def propietario(id):
     return jsonify(Matricula.getPropietario(id))


@app.route('/', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not Matricula.valid(data):
        abort(400)
    result = Matricula.add(data)
    return jsonify({'result': result}), 201

@app.route('/<int:id>', methods=['PUT'])
def update(id):
    temp = Matricula.get(id)
    data = request.get_json()
    if not temp or not data or not Matricula.valid(data):
        abort(404)
    result = Matricula.update(id, data)
    return jsonify({'result': result }), 201

@app.route('/<int:id>', methods=['DELETE'])
def destroy(id):
    temp = Matricula.get(id)
    if not temp: abort(404)
    result = Matricula.remove(id)
    return jsonify({'result': result }), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_first_request
def _run_on_start():
    Matricula.connect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
    # app.run(port=55555, debug=True)
