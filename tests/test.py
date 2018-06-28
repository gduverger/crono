import pytest


"""
python -m pytest tests/test.py
"""


def test():
	"""
	python -m pytest tests/test.py::test
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
