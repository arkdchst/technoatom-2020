import socket
import json

LINE_BREAK = '\r\n'

class HttpRequest:
	def __init__(self, method, host, port, path, headers=[], data=None):
		self.method = method
		self.host = host; self.port = port
		self.path = path
		self.headers = headers
		self.data = data
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(2)

	def request_first_line(self):
		return self.method + ' ' + self.path + ' HTTP/1.1' + LINE_BREAK

	def request_headers(self, content_length=None):
		if content_length:
			headers = self.headers + [f'Content-Length: {content_length}']
		else:
			headers = self.headers
		headers += ['Content-Type: application/json']
		return LINE_BREAK.join(headers) + LINE_BREAK + LINE_BREAK

	def request_data(self):
		if self.data:
			return json.dumps(self.data)
		else:
			return ''

	def do(self):
		self.send()
		data, status_code = self.receive()
		
		self.close()

		return data, status_code

	def send(self):
		self.socket.connect((self.host, self.port))

		request_data_encoded = self.request_data().encode()
		request_encoded = ( self.request_first_line() + self.request_headers(len(request_data_encoded)) ).encode() + request_data_encoded

		self.socket.sendall(request_encoded)

	def receive(self, bs=4096):
		data = bytes()
		while True:
			buf = None
			try:
				buf = self.socket.recv(bs)
			except socket.timeout:
				pass
			if not buf:
				break

			data += buf


		str_ = data.decode()
		
		first_space = str_.find(' ')
		status_code = int(str_[first_space + 1 : first_space + 4])

		str_ = str_[str_.find('\r\n\r\n') + 4 : ] # skip all headers
		try:
			return json.loads(str_), status_code
		except json.decoder.JSONDecodeError:
			return str_, status_code

	def close(self):
		self.socket.close()