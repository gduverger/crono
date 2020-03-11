import pytest

from crono import utils


"""
python -m pytest tests/test_utils.py
"""


def test_seconds():
	"""
	python -m pytest tests/test_utils.py::test_seconds
	"""

	assert utils.seconds(seconds=42) == 42
	assert utils.seconds(minutes=42) == 42 * 60
	assert utils.seconds(hours=42) == 42 * 60 * 60
	assert utils.seconds(minutes=42, seconds=42) == 42 + (42 * 60)
	assert utils.seconds(hours=42, minutes=42, seconds=42) == 42 + (42 * 60) + (42 * 60 * 60)


def test_class():
	"""
	python -m pytest tests/test_utils.py::test_class
	"""

	a = [1, 2, 3]

	class O:

		def __init__(self, a=None):
			self.a = a

	o = O(a=a)
	assert a == [1, 2, 3]
	assert o.a == [1, 2, 3]

	a = [4, 5, 6]
	assert a == [4, 5, 6]
	assert o.a != [4, 5, 6] # !

	o.a = [7, 8, 9]
	assert a != [7, 8, 9] # !
	assert o.a == [7, 8, 9]


def test_list():
	"""
	python -m pytest tests/test_utils.py::test_list
	"""

	assert [0, 1, 2] == [0, 1, 2]
	assert [0, 1, 2] != [2, 1, 0]

	assert all(x in [0, 1, 2] for x in [0, 1, 2])
	assert all(x in [0, 1, 2] for x in [2, 1, 0])
