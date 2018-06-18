import pytest

from apistar import exceptions
from api import schemas_new as schemas


class TestSchemas(object):
	"""
	python -m pytest tests/test_schemas_new.py::TestSchemas
	"""


	def test_interval_params(self):
		"""
		python -m pytest tests/test_schemas_new.py::TestSchemas::test_interval_params
		"""

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'This field is required.'}"):
			schemas.interval_params.validate({})

		with pytest.raises(exceptions.ValidationError, match='Must be an object.'):
			schemas.interval_params.validate({'foo'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'This field is required.', 'foo': 'Invalid property name.'}"):
			schemas.interval_params.validate({'foo': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'Must be a number.'}"):
			schemas.interval_params.validate({'seconds': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'Must be a number.'}"):
			schemas.interval_params.validate({'seconds': '10'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'Must be greater than or equal to 300.'}"):
			schemas.interval_params.validate({'seconds': 10})

		interval_params = schemas.interval_params.validate({'seconds': 300})
		assert interval_params['seconds'] == 300


	def test_interval(self):
		"""
		python -m pytest tests/test_schemas_new.py::TestSchemas::test_interval
		"""

		with pytest.raises(exceptions.ValidationError, match="{'name': 'This field is required.', 'params': 'This field is required.'}"):
			schemas.interval.validate({})

		# BUG
		with pytest.raises(KeyError):
			schemas.interval.validate({'name': 'foo', 'params': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'params': 'Must be an object.'}"):
			schemas.interval.validate({'name': 'interval', 'params': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'params': {'seconds': 'This field is required.'}}"):
			schemas.interval.validate({'name': 'interval', 'params': {}})

		with pytest.raises(exceptions.ValidationError, match="{'params': {'seconds': 'Must be a number.'}}"):
			schemas.interval.validate({'name': 'interval', 'params': {'seconds': 'foo'}})

		with pytest.raises(exceptions.ValidationError, match="{'params': {'seconds': 'Must be a number.'}}"):
			schemas.interval.validate({'name': 'interval', 'params': {'seconds': '10'}})

		with pytest.raises(exceptions.ValidationError, match="{'params': {'seconds': 'Must be greater than or equal to 300.'}}"):
			schemas.interval.validate({'name': 'interval', 'params': {'seconds': 10}})

		interval = schemas.interval.validate({'name': 'interval', 'params': {'seconds': 300}})
		assert interval['name'] == 'interval'
		assert interval['params'] == {'seconds': 300}
		assert interval['params']['seconds'] == 300
