#!/usr/bin/env python
from google_mock import google_mock
import google_word_manager
import request
import errors
import signal
import sys
import time

APP_ADDRESS =	{'host':'localhost', 'port':8090}
SERVER_ADDRESS ={'host':'localhost', 'port':8080}

USER = {'user': 'Brin'}
AUTH = 'Authorization: brins_password'


def req(path, method, number=None):
	number_dict = {}
	if number != None:
		number_dict = {'number': number}
	return request.HttpRequest(method=method, **APP_ADDRESS, path=path, headers=[AUTH], data={**USER, **number_dict}).do()



def start_app():
	def wait_until_loads():
		while True:
			try:
				req('/', 'GET')
				break
			except:
				pass

	google_word_manager.start(**APP_ADDRESS, server_address=f'http://{SERVER_ADDRESS["host"]}:{SERVER_ADDRESS["port"]}')
	wait_until_loads()


def shutdown_app():
	def wait_until_shuts_down():
			while True:
				try:
					req('/', 'GET')
				except:
					break
	req('/shutdown', 'GET')
	wait_until_shuts_down()


def start_mock():
	mock = google_mock.Server(**SERVER_ADDRESS)
	mock.start()
	return mock

def shutdown_mock(mock):
	mock.stop()


def main():
	mock = start_mock()
	start_app()

	def handle_sigint(sig, frame):
		shutdown_app()
		shutdown_mock(mock)
		sys.exit(0)

	signal.signal(signal.SIGINT, handle_sigint)

	while True:
		time.sleep(1)

if __name__ == "__main__":
	main()