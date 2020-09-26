import itertools
import pytest


def test_zerodivision():
	with pytest.raises(ZeroDivisionError):
		1 / 0
	with pytest.raises(ZeroDivisionError):
		0 / 0


@pytest.mark.parametrize('a,b', [(71, 16), (0, 0), (-30, 30), (0, 45), (-74, 90), (-11, -31)])
def test_sum_commutative(a, b):
	assert a + b == b + a


class TestMod:
	def test_mod(self):
		assert 70 % 5 == 0
		assert 0 % 5 == 0
		assert 1 % 5 == 1
		assert 2 % 1 == 0

	def test_mod_zerodivision(self):
		with pytest.raises(ZeroDivisionError):
			1 % 0
		with pytest.raises(ZeroDivisionError):
			0 % 0

def test_div():
	assert 10 // 2 == 5
	assert 10 // 3 == 3
	assert 1 // 3 == 0
	assert 0 // 3 == 0

def test_div_zerodivision():
	with pytest.raises(ZeroDivisionError):
		1 // 0
	with pytest.raises(ZeroDivisionError):
		0 // 0