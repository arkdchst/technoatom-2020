import pytest
import string
import random

from user import User
import config

def random_str(length=10):
	letters = string.ascii_letters
	return ''.join(random.choices(letters, k=length))

def gen_user():
	user = User(username = random_str(), password = random_str(), email = f'{random_str(5).lower()}@{random_str(5).lower()}.com', access=1)
	return user

def random_number(length=10):
	digits = string.digits
	non_zero = digits[1:]
	return int(''.join(random.choices(non_zero, k=1)) + ''.join(random.choices(digits, k=length-1)))


def rect_intersect(rectA, rectB):
	return (rectA['x']						<=	rectB['x'] + rectB['width']		and
			rectA['x'] + rectA['width']		>=	rectB['x']						and
			rectA['y']						<=	rectB['y'] + rectB['height']	and
			rectA['y'] + rectA['height']	>=	rectB['y'])

bug = pytest.mark.xfail(raises=AssertionError, reason='bug')