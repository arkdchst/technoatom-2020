import pytest


def test_append():
	l = []
	assert l == []
	l.append(1)
	assert l == [1]
	l.append(2)
	assert l == [1, 2]
	l.append(3)
	assert l == [1, 2, 3]


def test_remove():
	l = [1, 1, 2, 2, 3, 3]
	l.remove(2)
	assert l == [1, 1, 2, 3, 3]
	l.remove(1)
	assert l == [1, 2, 3, 3]
	l.remove(3)
	assert l == [1, 2, 3]
	l.remove(2); l.remove(3)
	assert l == [1]
	l.remove(1)
	assert l == []
	with pytest.raises(ValueError):
		l.remove(0)

def test_reverse():
	l = [1, 2, 3, 4]
	l.reverse()
	assert l == [4, 3, 2, 1]
	l = [1]
	l.reverse()
	assert l == [1]
	l = []
	l.reverse()
	assert l == []
	l = [1, 2]
	l.reverse()
	assert l == [2, 1]

class TestCount:
	def test_count(self):
		l = [1, 1, 1, 2, 2, 3]
		assert l.count(1) == 3
		assert l.count(2) == 2
		assert l.count(3) == 1
		assert l.count(4) == 0


sort_data = [
	([3, 5, 1, 4, 2], [1, 2, 3, 4, 5]),
	([3, 5, 1, 4, 3], [1, 3, 3, 4, 5]),
	([2, 1], [1, 2]),
	([1, 2], [1, 2]),
	([1], [1]),
	([], []),
]

@pytest.mark.parametrize('l,expected', sort_data)
def test_sort(l, expected):
	l.sort()
	assert l == expected