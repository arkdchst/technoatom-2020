import pytest

from config import MYAPP_URL
from helpers import bug

from api.client import Client, Codes
from db.fixtures import *

@pytest.fixture
def client(added_user):
	client = Client()
	user = gen_user()
	with added_user(user) as user:
		client.login(user.username, user.password)
		yield client

def test_not_authorized(connection, added_user_del):
	"""Test that without called /login we have no access to api."""
	user = gen_user()
	with added_user_del(user):
		res = Client().add_user(user.username, user.password, user.email)

		assert not connection.get_user(user.username)
		assert res.status_code == Codes.NOT_AUTHORIZED

def test_bad_request(connection, client, added_user_del):
	"""Test that if request is bad api returns BAD_REQUEST."""
	with added_user_del() as user:
		# form data instead of json
		res = client.session.post(f'{MYAPP_URL}/api/add_user', data={'username': user.username, 'password': user.password, 'email': user.email})

		assert res.status_code == Codes.BAD_REQUEST


class TestAdd:
	"""Test add_user method."""

	def test(self, connection, client, added_user_del):
		"""Test fields in user record in DB after called add_user. Test also status code."""
		with added_user_del() as user:
			res = client.add_user(user.username, user.password, user.email)
			db_user = connection.get_user(user.username)
			assert db_user
			assert db_user.username == user.username
			assert db_user.password == user.password
			assert db_user.email == user.email
			assert db_user.access == 1

			assert res.status_code == Codes.ADDED

	def test_existing_username_code(self, connection, client, added_user_del):
		"""Test that if user with same username already exists api returns EXISIS."""
		with added_user_del() as user:
			client.add_user(user.username, user.password, user.email)
			new_user = gen_user()
			res = client.add_user(user.username, new_user.password, new_user.email)

			assert res.status_code == Codes.EXISIS

	@bug
	def test_existing_email_code(self, connection, client, added_user_del):
		"""Test that if user with same email already exists api returns EXISIS."""
		with added_user_del() as user:
			client.add_user(user.username, user.password, user.email)
			new_user = gen_user()
			res = client.add_user(new_user.username, new_user.password, user.email)

			assert res.status_code == Codes.EXISIS

	@bug
	def test_val_short_username(self, connection, client, added_user_del):
		"""Test that short username is not accepted such as in UI."""
		user = gen_user()
		user.username = random_str(5)
		with added_user_del() as user:
			res = client.add_user(user.username, user.password, user.email)
			assert not connection.get_user(user.username)

	@bug
	def test_val_empty_password(self, connection, client, added_user_del):
		"""Test that empty password is not accepted such as in UI."""
		user = gen_user()
		user.password = ''
		with added_user_del() as user:
			res = client.add_user(user.username, user.password, user.email)
			assert not connection.get_user(user.username)


	@bug
	def test_val_bad_email(self, connection, client, added_user_del):
		"""Test that bad username is not accepted such as in UI."""
		user = gen_user()
		user.email = random_str()
		with added_user_del() as user:
			res = client.add_user(user.username, user.password, user.email)
			assert not connection.get_user(user.username)


	@bug
	def test_code(self, connection, client, added_user_del):
		"""Test that status code if entity is added is 201."""
		with added_user_del() as user:
			res = client.add_user(user.username, user.password, user.email)
			assert res.status_code == Codes.ADDED_FROM_DOCS

class TestDel:
	"""Test del_user method."""

	def test(self, connection, client, added_user):
		"""Test that after deleting there is no user record in DB. Test also status code is DELETED."""
		with added_user() as user:
			res = client.del_user(user.username)
			assert not connection.get_user(user.username)
			assert res.status_code == Codes.DELETED

	def test_not_exists(self, connection, client, added_user):
		"""Test that if there is no user with given username API returns NOT_EXISTS."""
		with added_user() as user:
			res = client.del_user(random_str())
			assert res.status_code == Codes.NOT_EXISTS

	def test_self(self, connection, client):
		"""Test that we can delete user as which we are logged in."""
		res = client.del_user(client.username)
		assert not connection.get_user(client.username)
		assert res.status_code == Codes.DELETED

class TestBlock:
	"""Test block_user method."""

	def test(self, connection, client, added_user):
		"""Test that after block_user access=0."""
		with added_user() as user:
			res = client.block_user(user.username)
			assert connection.get_user(user.username).access == 0
			assert res.status_code == Codes.DONE

	def test_block_blocked(self, connection, client, added_user):
		"""Test that after repeat block access remains 0."""
		with added_user() as user:
			client.block_user(user.username)
			res = client.block_user(user.username)

			assert connection.get_user(user.username).access == 0
			assert res.status_code == Codes.EXISIS

class TestAccept:
	"""Test accept_user method."""

	def test(self, connection, client, added_user):
		"""Test that after accept_user access=1."""
		user = gen_user()
		user.access = 0
		with added_user(user=user) as user:
			res = client.accept_user(user.username)
			assert connection.get_user(user.username).access == 1
			assert res.status_code == Codes.DONE

	def test_accept_accepted(self, connection, client, added_user):
		"""Test that after repeat accept access remains 1."""
		with added_user() as user: # accepted by default
			res = client.accept_user(user.username)

			assert connection.get_user(user.username).access == 1
			assert res.status_code == Codes.EXISIS

def test_status(client):
	"""Test that status return 'ok'"""
	assert client.status()['status'] == 'ok'
