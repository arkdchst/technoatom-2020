import pytest


def test_concat():
	assert '' + '' == ''
	assert 'abc' + '' == 'abc'
	assert '' + 'abc' == 'abc'
	assert 'abc' + 'def' == 'abcdef'

def test_len():
	assert len('') == 0
	assert len('a') == 1
	assert len('abc') == 3

def test_upper():
	assert ''.upper() == ''
	assert 'a'.upper() == 'A'
	assert 'abc'.upper() == 'ABC'


class TestStrip:
	def test_strip(self):
		assert ''.strip() == ''
		assert 'abc'.strip() == 'abc'
		assert ' abc'.strip() == 'abc'
		assert ' \tabc \t'.strip() == 'abc'
		assert 'AABAabcABA'.strip('AB') == 'abc'


@pytest.mark.parametrize('s,sub,expected', [('abcdef', 'a', 0), ('abcdef', 'b', 1), ('abcdef', 'f', 5)])
def test_index(s, sub, expected):
	assert s.index(sub) == expected

def test_index_bad():
	with pytest.raises(ValueError):
		assert ''.index('a')
		assert 'abc'.index('d')
