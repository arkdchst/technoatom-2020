from flask import Flask, request, jsonify, session

app = Flask(__name__)

@app.route('/vk_id/<username>', methods=['GET'])
def get_id(username):
	if username in app.config.userdata:
		return {'vk_id': app.config.userdata[username]}
	else:
		return {}, 404

@app.route('/service/set', methods=['POST'])
def set():
	json = request.get_json()

	username = json['username']
	id = json['id']

	assert isinstance(username, str)
	assert isinstance(id, int)

	app.config.userdata[username] = id

	return '', 204 # no content

@app.route('/service/unset/<username>', methods=['GET'])
def unset(username):
	del app.config.userdata[username]

	return '', 204

if __name__ == '__main__':
	app.config.userdata = {}
	app.run(host='0.0.0.0', port=8082)