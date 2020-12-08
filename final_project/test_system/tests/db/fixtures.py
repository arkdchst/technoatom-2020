import requests
import pytest
from sqlalchemy.ext.automap import automap_base
from time import sleep
from contextlib import contextmanager

from helpers import *
from config import *

import db.connection

@pytest.fixture
def connection():
	connection = db.connection.Connection(db_name=MYAPP_DB_NAME, user=MYAPP_DB_USER, password=MYAPP_DB_PASSWORD, host=MYAPP_DB_HOST, port=MYAPP_DB_PORT)

	yield connection


@pytest.fixture
def added_user_add(connection):
	@contextmanager
	def gen(user=None):
		if not user:
			user = gen_user()

		connection.add_user(user)

		yield user
	return gen

@pytest.fixture
def added_user_del(connection): # guarantees that created user will be deleted
	@contextmanager
	def gen(user=None):
		if not user:
			user = gen_user()
		
		try:	
			yield user
		finally:
			connection.del_user(user.username)

	return gen


@pytest.fixture
def added_user(connection, added_user_add, added_user_del):
	@contextmanager
	def gen(user=None):
		with added_user_add(user) as user:
			with added_user_del(user):
				yield user


	return gen
