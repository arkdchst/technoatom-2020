import socket
from threading import Thread


class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port

	def _loop(self):
		while not self.stop_flag:
			try:
				conn, _ = self.server_socket.accept()
				if self.send_500:
					self._receive(conn)
					conn.sendall('HTTP/1.1 500 Internal Server Error\r\nConnection: close\r\n\r\n'.encode())
					conn.close()
				else:
					self.clients.append(conn)
			except socket.timeout:
				pass

	def _receive(self, conn):
		conn.settimeout(0.1)
		while True:
			buf = None
			try:
				buf = conn.recv(4096)
			except socket.timeout:
				pass
			if not buf:
				break


	# if not send_500 then listen only but no answer
	# if send_500 is true then answer with code 500
	def start(self, send_500=False):
		self.send_500 = send_500
		self.stop_flag = False

		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.settimeout(0.1)

		self.clients = []

		# this prevents 'OSError: [Errno 98] Address already in use', see https://docs.python.org/3/library/socket.html#example
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.server_socket.bind((self.host, self.port))
		self.server_socket.listen()

		self.th = Thread(target=self._loop, daemon=True)
		self.th.start()

	def stop(self):
		self.stop_flag = True

		for client in self.clients:
			client.close()

		self.server_socket.close()
		self.th.join()
