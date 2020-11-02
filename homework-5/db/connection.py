import sqlalchemy
from sqlalchemy.orm import sessionmaker


class Connection:

	def __init__(self, db_name, user='root', password='', host='localhost', port=3306):
		self.user = user
		self.password = password
		self.host = host
		self.port = port
		self.db_name = db_name


	def get_connection(self, db_created):
		engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
			user=self.user,
			password=self.password,
			host=self.host,
			port=self.port,
			db=self.db_name if db_created else ''
		))
		return engine.connect()

	def drop_db(self):
		connection = self.get_connection(False)
		connection.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
		connection.close()

	def connect(self):
		connection = self.get_connection(False)
		connection.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_name}')
		connection.close()

		self.connection = self.get_connection(True)

	def engine(self):
		return self.connection.engine

	def session(self):
		return sessionmaker(bind=self.connection)()