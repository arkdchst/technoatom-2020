import pytest
from db.connection import Connection
from db.models import TaskA, Base


@pytest.fixture
def connection():
	connection = Connection(password='YOUR_MYSQL_PASSWORD', db_name='test')
	connection.drop_db()
	connection.connect()

	yield connection

	connection.drop_db()


def test(connection):
	session = connection.session()
	TaskA.__table__.create(connection.engine())

	task = TaskA(result=1)

	session.add(task)
	session.commit()

	assert session.query(TaskA).all() == [task]

	session.close()