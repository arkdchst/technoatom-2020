from threading import Thread
import requests
from flask import Flask, request, jsonify, session
import functools
import errors
import json

app = Flask(__name__)



class Server_Returned_Error(Exception):
	pass


def req(method, *args, **kwargs):
	res = requests.request(method, *args, **kwargs, timeout=1)
	if not res.status_code in range(200,300):
		try:
			json_ = res.json()
			if 'error' in json_:
				raise Server_Returned_Error(json_['error'], res.status_code)
		except json.decoder.JSONDecodeError:
			pass

		raise Server_Returned_Error(res.text, res.status_code)

	return res

def get_req(*args, **kwargs):
	return req('GET', *args, **kwargs)

def post_req(*args, **kwargs):
	return req('POST', *args, **kwargs)


def error_ready(f): # wraps function that requests external server to handle connection errors
	@functools.wraps(f)
	def new_fun(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except requests.exceptions.Timeout:
			return jsonify({'error': errors.SERVER_TIMEOUT}), 500
		except requests.exceptions.ConnectionError:
			return jsonify({'error': errors.SERVER_CONN_REFUSED}), 500
		except Server_Returned_Error as e:
			return jsonify({'message': errors.SERVER_RETURNED_ERROR, 'error': e.args[0], 'code': e.args[1]}), 500

	return new_fun



def start(host, port, server_address):
	server = Thread(target=app.run, kwargs={'host': host, 'port': port}, daemon=True)

	app.config['server_address'] = server_address # o-letters number management server

	server.start()

@app.route('/shutdown')
def stop():
	terminate_func = request.environ.get('werkzeug.server.shutdown')
	if terminate_func:
		terminate_func()

	return 'bye'

def get_auth_header():
	return {'Authorization': request.headers['Authorization']} if 'Authorization' in request.headers else None


@app.route('/number/<any(increase, decrease):action>', methods=['POST'])
@error_ready
def increase(action):
	if not 'user' in request.json:
		return errors.AUTH_REQUIRED, 401

	res = post_req(app.config['server_address'] + '/number/' + action, json={'user': request.json['user']},
						 headers=get_auth_header())
	return res.text, res.status_code


@app.route('/number/set', methods=['POST'])
@error_ready
def set():
	if not 'user' in request.json:
		return errors.AUTH_REQUIRED, 401
	if not 'number' in request.json:
		return errors.NUMBER_REQUIRED, 400

	res = post_req(app.config['server_address'] + '/number/set', json={'user': request.json['user'], 'number': request.json['number']},
						 headers=get_auth_header())
	return res.text, res.status_code

@app.route('/number', methods=['GET'])
@app.route('/number/get', methods=['GET'])
@error_ready
def get_number():
	return jsonify(get_req(app.config['server_address'] + '/number').json()['number'])

@app.route('/', methods=['GET'])
@app.route('/word', methods=['GET'])
@app.route('/word/get', methods=['GET'])
@error_ready
def get_word():
	return jsonify(get_req(app.config['server_address'] + '/word').json()['word'])
