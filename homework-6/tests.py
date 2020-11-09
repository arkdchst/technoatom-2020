from google_mock import google_mock
import google_word_manager
import google_stub
import pytest
import request
import errors

APP_ADDRESS =	{'host':'localhost', 'port':8090}
SERVER_ADDRESS ={'host':'localhost', 'port':8080}

USER = {'user': 'Brin'}
AUTH = 'Authorization: brins_password'


def req(path, method, number=None):
	number_dict = {}
	if number != None:
		number_dict = {'number': number}
	return request.HttpRequest(method=method, **APP_ADDRESS, path=path, headers=[AUTH], data={**USER, **number_dict}).do()

def is_ok(status):
	return status in range(200,300)



@pytest.fixture(scope='session', autouse=True)
def app():
	def wait_until_loads():
		while True:
			try:
				req('/', 'GET')
				break
			except:
				pass

	def wait_until_shuts_down():
		while True:
			try:
				req('/', 'GET')
			except:
				break


	google_word_manager.start(**APP_ADDRESS, server_address=f'http://{SERVER_ADDRESS["host"]}:{SERVER_ADDRESS["port"]}')
	wait_until_loads()

	yield

	req('/shutdown', 'GET')
	wait_until_shuts_down()


@pytest.fixture(scope='class')
def mock():
	mock = google_mock.Server(**SERVER_ADDRESS)
	mock.start()
	yield
	mock.stop()


@pytest.fixture(scope='class')
def _base_stub():
	stub = google_stub.Server(**SERVER_ADDRESS)
	yield stub
	stub.stop()

@pytest.fixture(scope='class')
def stub(_base_stub):
	_base_stub.start()
	yield

@pytest.fixture(scope='class')
def stub_500(_base_stub): # stub that returns 500
	_base_stub.start(send_500=True)
	yield



@pytest.mark.usefixtures('mock')
class Test_Mock_Up:

	def test_increase(self):
		current = req('/number/set', 'POST', 4)[0]['number']
		assert req('/number/increase', 'POST')[0]['number'] == current + 1
		current = req('/number/set', 'POST', 0)[0]['number']
		assert req('/number/increase', 'POST')[0]['number'] == current + 1

	def test_decrease(self):
		current = req('/number/set', 'POST', 4)[0]['number']
		assert req('/number/decrease', 'POST')[0]['number'] == current - 1
		current = req('/number/set', 'POST', 0)[0]['number']
		assert not is_ok(req('/number/decrease', 'POST')[1])

	def test_set(self):
		req('/number/set', 'POST', 0)
		req('/number/set', 'POST', 10)
		assert req('/number/get', 'GET')[0] == 10
		assert not is_ok(req('/number/set', 'POST', -5)[1])

	def test_word_get(self):
		req('/number/set', 'POST', 3)
		assert req('/word/get', 'GET')[0] == 'Gooogle'

	def test_number_get(self):
		req('/number/set', 'POST', 3)
		assert req('/number/get', 'GET')[0] == 3


	def test_no_header(self):
		res = request.HttpRequest(method='POST', **APP_ADDRESS, path='/number/increase', headers=[], data={**USER}).do()
		assert not is_ok(res[1])
		assert res[0]['message'] == errors.SERVER_RETURNED_ERROR # check that error created exactly by the server but not by application
		assert res[0]['error'] == errors.AUTH_NO_HEADER

	def test_bad_header(self):
		res = request.HttpRequest(method='POST', **APP_ADDRESS, path='/number/increase', headers=['Authorization: bad_password'], data={**USER}).do()
		assert not is_ok(res[1])
		assert res[0]['error'] == errors.AUTH_BAD

	def test_bad_user(self):
		res = request.HttpRequest(method='POST', **APP_ADDRESS, path='/number/increase', headers=[AUTH], data={'user': 'bad_user'}).do()
		assert not is_ok(res[1])
		assert res[0]['error'] == errors.AUTH_BAD


def test_server_down():
	res = req('/word', 'GET')
	assert not is_ok(res[1])
	assert res[0]['error'] == errors.SERVER_CONN_REFUSED

def test_server_timeout(stub):
	res = req('/word', 'GET')
	assert not is_ok(res[1])
	assert res[0]['error'] == errors.SERVER_TIMEOUT

def test_server_internal_error(stub_500):
	res = req('/word', 'GET')
	assert not is_ok(res[1])
	assert res[0]['message'] == errors.SERVER_RETURNED_ERROR
	assert res[0]['code'] == 500

