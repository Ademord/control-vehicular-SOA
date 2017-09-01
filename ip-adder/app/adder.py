#!flask/bin/python
from flask import Flask, jsonify, abort, request
from redis import Redis
app = Flask(__name__)

redis_conn = Redis(host='redis')

@app.route('/', methods=['POST'])
def addToQueue():
    data = request.get_json()
    if not request.json or not 'queue' in data or not 'body' in data:
        abort(400)

    redis_conn.rpush(data['queue'], data['body'])
    return jsonify({'result': 'Added ' + data['body']}), 201

@app.route('/publish/', methods=['POST'])
def publish():
    data = request.get_json()
    if not request.json or not 'channel' in data or not 'body' in data:
        abort(400)

    redis_conn.publish(data['channel'], data['body'])
    return jsonify({'result': 'Added ' + data['body']}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
    # IP_QUEUE = 'ip'
    # data = { 'ip': '123.123.123' }
    # redis_conn.rpush(IP_QUEUE, data['ip'])

    