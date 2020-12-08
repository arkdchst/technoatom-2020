import requests

from config import MYAPP_URL
from helpers import *

class Codes():
	ADDED = 210
	EXISIS = 304
	DELETED = 204
	BAD_REQUEST = 400
	NOT_EXISTS = 404
	NOT_AUTHORIZED = 401
	DONE = 200

	ADDED_FROM_DOCS = 201 # true code is ADDED, but 201 stands in documentation

class Client():

	def __init__(self):
		self.session = requests.Session()

	def login(self, username, password):
		self.username = username
		self.password = password

		return self.session.post(f'{MYAPP_URL}/login', data={'username': self.username, 'password': self.password, 'submit':'Login'})

	def add_user(self, username, password, email):
		return self.session.post(f'{MYAPP_URL}/api/add_user', json={'username': username, 'password': password, 'email': email})

	def del_user(self, username):
		return self.session.get(f'{MYAPP_URL}/api/del_user/{username}')

	def block_user(self, username):
		return self.session.get(f'{MYAPP_URL}/api/block_user/{username}')

	def accept_user(self, username):
		return self.session.get(f'{MYAPP_URL}/api/accept_user/{username}')

	def status(self):
		return self.session.get(f'{MYAPP_URL}/status').json()
