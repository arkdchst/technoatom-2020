
class User:
	def __init__(self, id=None, username=None, password=None, email=None, access=None, active=None, start_active_time=None):
		self.id = id
		self.username = username
		self.password = password
		self.email = email
		self.access = access
		self.active = active
		self.start_active_time = start_active_time