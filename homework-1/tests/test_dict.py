import pytest

def test_set():
	d = {}
	d['one'] = 1
	assert d == {'one': 1}
	d['two'] = 2
	assert d == {'one': 1, 'two': 2}
	d['one'] = 3
	assert d == {'one': 3, 'two': 2}

def test_pop():
	d = {'one': 1, 'two': 2, 'three': 3}
	assert d.pop('two') == 2
	assert d == {'one': 1, 'three': 3}

	assert d.pop('three') == 3
	assert d == {'one': 1}

	with pytest.raises(KeyError):
		d.pop('three')

	assert d.pop('one') == 1
	assert d == {}

class TestPopitem:
	def test_popitem(self):
		d = {}
		d['one'] = 1
		d['two'] = 2
		d['three'] = 3
		assert d.popitem() == ('three', 3)
		assert d == {'one': 1, 'two': 2}

		assert d.popitem() == ('two', 2)
		assert d == {'one': 1}

		assert d.popitem() == ('one', 1)
		assert d == {}

		with pytest.raises(KeyError):
			d.popitem()


@pytest.mark.parametrize('n', range(10))
def test_len(n):
	d = {}
	for i in range(n):
		d[i] = None
	assert len(d) == n


def test_get():
	d = {'one': 1, 'two': 2, 'three': 3}
	assert d.get('one') == 1
	assert d.get('two') == 2
	assert d.get('three') == 3
	assert d.get('four') == None
	assert d.get('four', 4) == 4

