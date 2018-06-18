import pytest

from apistar import exceptions
from api import schemas_new as schemas


class TestSchemas(object):
	"""
	python -m pytest tests/test_schemas_new.py::TestSchemas
	"""


	def test_trigger_interval_params(self):
		"""
		python -m pytest tests/test_schemas_new.py::TestSchemas::test_trigger_interval_params
		"""

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'This field is required.'}"):
			schemas.trigger_interval_params.validate({})

		with pytest.raises(exceptions.ValidationError, match='Must be an object.'):
			schemas.trigger_interval_params.validate({'foo'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'This field is required.', 'foo': 'Invalid property name.'}"):
			schemas.trigger_interval_params.validate({'foo': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'Must be a number.'}"):
			schemas.trigger_interval_params.validate({'seconds': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'Must be a number.'}"):
			schemas.trigger_interval_params.validate({'seconds': '10'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'Must be greater than or equal to 300.'}"):
			schemas.trigger_interval_params.validate({'seconds': 10})

		trigger_interval_params = schemas.trigger_interval_params.validate({'seconds': 300})
		assert trigger_interval_params['seconds'] == 300


	def test_trigger_interval(self):
		"""
		python -m pytest tests/test_schemas_new.py::TestSchemas::test_trigger_interval
		"""

		with pytest.raises(exceptions.ValidationError, match="{'name': 'This field is required.', 'params': 'This field is required.'}"):
			schemas.trigger_interval.validate({})
