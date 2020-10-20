import pytest
from client import Client

@pytest.mark.api
class TestApi:
	@pytest.fixture(autouse=True)
	def setup(self):
		self.client = Client()

	@pytest.fixture
	def auth(self):
		self.client.auth('fidorig277@zik2zik.com', 'fidorig277')


	def test_add(self, auth):
		id_ = self.client.add_segment()
		assert self.client.segment_exists(id_)
		self.client.delete_segment(id_)


	def test_delete(self, auth):
		id_ = self.client.add_segment()

		self.client.delete_segment(id_)
		assert not self.client.segment_exists(id_)
