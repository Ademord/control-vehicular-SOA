#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import lugar
app = Flask(__name__)

@app.route('/lugares', methods=['GET'])
def index():
    lugares = lugar.getall()
    return jsonify({'lugares': lugares})

@app.route('/lugares/<int:id>', methods=['GET'])
def show(id):
    temp = lugar.get(id)
    if not temp: abort(404)
    return jsonify({'lugar': temp})

@app.route('/lugares', methods=['POST'])
def store():
    data = request.get_json()
    if not request.json or not 'title' in request.json:
        abort(400)
    result = lugar.add(data)
    return jsonify({'result': True}), 201

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

if __name__ == '__main__':
    print("hola")
    app.run(host='0.0.0.0', port=55555, debug=True)
    print("chau")