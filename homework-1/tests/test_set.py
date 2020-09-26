import pytest

def test_add():
	s = set()
	s.add(1)
	assert s == {1}
	s.add(1)
	assert s == {1}
	s.add(2)
	assert s == {1, 2}
	s.add(2)
	assert s == {1, 2}
	s.add(3)
	assert s == {1, 2, 3}

def test_remove():
	s = {1, 2, 3}
	s.remove(2)
	assert s == {1, 3}
	s.remove(3)
	assert s == {1}
	with pytest.raises(KeyError):
		s.remove(3)
	s.remove(1)
	assert s == set()

def test_intersection():
	assert {1, 2, 3}.intersection({2, 3}) == {2, 3}
	assert {1, 2, 3}.intersection({2}) == {2}
	assert set().intersection({1, 2}) == set()
	assert {1, 2, 3}.intersection({1, 2, 3}) == {1, 2, 3}
	assert {1, 2, 3}.intersection(set()) == set()

class TestUnion:
	def test_union(self):
		assert set().union({1, 2, 3}) == {1, 2, 3}
		assert {1, 2, 3}.union({1, 2, 3}) == {1, 2, 3}
		assert {1, 2}.union({1, 2, 3}) == {1, 2, 3}
		assert {1, 2}.union({3}) == {1, 2, 3}


subset_data = [
	({1, 2}, {1, 2, 3}, True),
	({1, 2, 4}, {1, 2, 3}, False),
	({1}, {1, 2, 3}, True),
	(set(), {1, 2, 3}, True),
	(set(), set(), True),
	({1}, set(), False),
]

@pytest.mark.parametrize('sub,uper,expected', subset_data)
def test_issubset(sub, uper, expected):
	assert sub.issubset(uper) == expected