from locust import HttpUser, TaskSet, task, between, constant


class NumberTasks(TaskSet):
	def on_start(self):
		self.client.headers['Authorization'] = 'brins_password'

	@task(2)
	def increase(self):
		self.client.post('/number/increase', json={'user':'Brin'})

	@task
	def decrease(self):
		self.client.post('/number/decrease', json={'user':'Brin'})

	@task
	def set(self):
		self.client.post('/number/set', json={'user':'Brin', 'number': 2})

	@task
	def number(self):
		self.client.get('/number')

	@task
	def number_get(self):
		self.client.get('/number/get')



class WordTasks(TaskSet):
	wait_time = constant(0.5)

	@task
	def word(self):
		self.client.get('/word')

	@task
	def word_get(self):
		self.client.get('/word/get')


class User(HttpUser):
	tasks = [NumberTasks, WordTasks]
	wait_time = between(1, 2)
