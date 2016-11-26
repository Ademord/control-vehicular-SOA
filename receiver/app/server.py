#!flask/bin/python
from flask import Flask, jsonify, request
app = Flask(__name__)

logs = [
	{
		'mensaje':'log inicial'
	}
]
@app.route('/receive', methods=['POST'])
def receive():
	data = request.get_json()
	logs.append(data)

@app.route('/', methods=['GET'])
def index():
	return jsonify({'logs': logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
