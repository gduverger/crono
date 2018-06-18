import pytest

from apistar import exceptions, validators


class TestApistar(object):
	"""
	python -m pytest tests/test_apistar.py::TestApistar
	"""


	def test_validators(self):
		"""
		python -m pytest tests/test_apistar.py::TestApistar::test_validators
		"""

		validator = validators.String(enum=['foo', 'bar'])
		assert validator.validate('foo')
		with pytest.raises(exceptions.ValidationError):
			validator.validate('eee')

		validator = validators.Array(items=[validators.String(enum=['foo', 'bar'])])
		assert validator.validate(['foo'])
		with pytest.raises(exceptions.ValidationError):
			validator.validate(['eee'])

		validator = validators.String(pattern='[^\s]* [^\s]* [^\s]* [^\s]* [^\s]*')
		assert validator.validate('*/10 * * * *')
