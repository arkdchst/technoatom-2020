import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from .google_word import GoogleWord
import errors

# only these users allowed to access o-letters number
users = {'Brin': 'brins_password', 'Page': 'pages_password'}


class Handler(BaseHTTPRequestHandler):
	def read_data(self):
		data = self.rfile.read(int(self.headers['Content-Length']))
		data = json.loads(data)

		self.data = data

	def get_user(self):
		return self.data['user']

	def get_number(self):
		return int(self.data['number'])

	def process_action(self):
		if self.path == '/number/set':
			if self.get_number() < 0:
				self.send_data({'error': errors.NUMBER_NEGATIVE}, 400)
				return False
			self.google_word.o_letters = int(self.get_number())
		elif self.path == '/number/increase':
			self.google_word.o_letters += 1
		elif self.path == '/number/decrease':
			if self.google_word.o_letters == 0:
				self.send_data({'error': errors.NUMBER_NEGATIVE}, 400)
				return False
			self.google_word.o_letters -= 1
		else:
			self.send_data({'error': errors.ACTION_BAD}, 400)
			return False

		return True

	def send_data(self, data, code=200):
		self.send_response(code)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps(data).encode())

	def do_GET(self):
		if self.path == '/word':
			self.send_data({'word': str(self.google_word)})
		elif self.path == '/number' or self.path == '/number/get':
			self.send_data({'number': self.google_word.o_letters})

	def do_POST(self):
		if not 'Authorization' in self.headers:
			self.send_data({'error': errors.AUTH_NO_HEADER}, 401)
			return

		self.read_data()
		user = self.get_user()
		password = self.headers['Authorization']
		if not (user in users and users[user] == password):
			self.send_data({'error': errors.AUTH_BAD}, 401)
			return

		if self.process_action():
			self.send_data({'message': 'successfully set value', 'number': self.google_word.o_letters})

	def do_PUT(self):
		self.do_POST()

	def handle_one_request(self, *args, **kwargs): # wrap parent's handle_one_request() method
		try:
			super().handle_one_request(*args, **kwargs)
		except Exception as e:
			self.send_error(400)

			from traceback import format_exc
			print(format_exc())


class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.server = HTTPServer((host, port), Handler)
		self.google_word = GoogleWord()
		Handler.google_word = self.google_word

	def start(self):
		self.th = Thread(target=self.server.serve_forever, daemon=True)
		self.th.start()

	def stop(self):
		self.server.shutdown()
		self.th.join()
		self.server.server_close()