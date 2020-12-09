from db.connection import Connection
from tasks import Tasks
from db.models import Base

def main():
	tasks = Tasks()
	connection = Connection(password='YOUR_MYSQL_PASSWORD', db_name='analyzed')
	connection.drop_db()
	connection.connect()

	Base.metadata.create_all(connection.engine())

	session = connection.session()
	for task in tasks.task_a, tasks.task_b, tasks.task_c, tasks.task_d, tasks.task_e:
		session.add_all(task())
	session.commit()

	session.close()

if __name__ == '__main__':
	main()