#!flask/bin/python
from flask import Flask, jsonify, abort, request
from redis import Redis
app = Flask(__name__)

redis_conn = Redis(host='redis')
IP_QUEUE = 'ip'

@app.route('/', methods=['POST'])
def request_recolector():
    data = request.get_json()
    if not request.json or not 'ip' in data:
        abort(400)

    print(redis_conn)
    redis_conn.rpush(IP_QUEUE, data['ip'])
    return jsonify({
        'result': 'Added ' + data['ip']
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
    # IP_QUEUE = 'ip'
    # data = { 'ip': '123.123.123' }
    # redis_conn.rpush(IP_QUEUE, data['ip'])

    