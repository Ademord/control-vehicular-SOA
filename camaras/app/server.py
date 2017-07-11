#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from app import Camara
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify(Camara.getall())

@app.route('/<int:id>', methods=['GET'])
def show(id):
    return jsonify(Camara.get(id))

@app.route('/search/<string:q>', methods=['GET'])
def search(q):
    return jsonify(Camara.buscar(q))

@app.route('/', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not Camara.valid(data):
        abort(400)
    return Camara.add(data)

@app.route('/<int:id>', methods=['PUT'])
def update(id):
    temp = Camara.get(id)
    data = request.get_json()
    if not temp or not data or not Camara.valid(data):
        abort(404)
    return Camara.update(id, data)

@app.route('/<int:id>', methods=['DELETE'])
def destroy(id):
    temp = Camara.get(id)
    if not temp: abort(404)
    return Camara.remove(id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_first_request
def _run_on_start():
    Camara.connect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55551, debug=True)
    # app.run(port=55555, debug=True)
