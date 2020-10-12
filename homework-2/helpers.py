import string
import random


def random_name(length=20):
	letters = string.ascii_letters
	return ''.join(random.choices(letters, k=length))