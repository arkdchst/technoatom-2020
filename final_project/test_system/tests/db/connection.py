import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from user import User

class Connection:

	def __init__(self, db_name, user='root', password='', host='localhost', port=3306):
		self.user = user
		self.password = password
		self.host = host
		self.port = port
		self.db_name = db_name

		self.connect()
		self.create_session()

		Base = automap_base()
		Base.prepare(self.engine(), reflect=True)

		self.table = Base.classes.test_users

	def get_connection(self, db_created):
		engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
			user=self.user,
			password=self.password,
			host=self.host,
			port=self.port,
			db=self.db_name if db_created else ''
		))
		return engine.connect()

	def connect(self):
		self.connection = self.get_connection(True)

	def engine(self):
		return self.connection.engine

	def create_session(self):
		self.session = sessionmaker(bind=self.connection)()

	def add_user(self, user):
		user_row = self.table(id=user.id, username=user.username, password=user.password, email=user.email, access=user.access, active=user.active, start_active_time=user.start_active_time)
		self.session.add(user_row)
		self.session.commit()

		user.id = user_row.id

	def _del_user_row(self, user_row):
		if user_row:
			self.session.delete(user_row)
		self.session.commit()

	def _row_to_user(self, user_row):
		if user_row:
			return User(id=user_row.id, username=user_row.username, password=user_row.password, email=user_row.email, access=user_row.access, active=user_row.active, start_active_time=user_row.start_active_time)

	def del_user(self, username):
		self.refresh()
		user_row = self.session.query(self.table).filter_by(username=username).one_or_none()
		self._del_user_row(user_row)

	def get_user_by_id(self, id):
		self.refresh()
		user_row = self.session.query(self.table).filter_by(id=id).one_or_none()

		return self._row_to_user(user_row)

	def get_user(self, username):
		self.refresh()
		user_row = self.session.query(self.table).filter_by(username=username).one_or_none()

		return self._row_to_user(user_row)

	def update_user(self, username, user):
		self.refresh()
		user_row = self.session.query(self.table).filter_by(username=username).one_or_none()

		user_row.password = user.password
		user_row.email = user.email
		user_row.access = user.access
		user_row.active = user.active
		user_row.start_active_time = user.start_active_time

		self.refresh()

	def refresh(self):
		self.session.commit()
