
class GoogleWord:
	def __init__(self, o_letters=2):
		self.o_letters = o_letters # number of letters 'o' in word 'Google'

	def __str__(self):
		return 'G' + 'o' * self.o_letters + 'gle'
