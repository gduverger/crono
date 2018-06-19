import os
import json
import pytest

from apistar import exceptions
from api import schemas


class TestSchemas(object):
	"""
	python -m pytest tests/test_schemas.py::TestSchemas
	"""


	def test_interval_params(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_interval_params
		"""

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'The \"seconds\" field is required.'}"):
			schemas.interval_params.validate({})

		with pytest.raises(exceptions.ValidationError, match='Must be an object.'):
			schemas.interval_params.validate({'foo'})

		with pytest.raises(exceptions.ValidationError, match="{'seconds': 'The \"seconds\" field is required.', 'foo': 'Invalid property name.'}"):
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
		python -m pytest tests/test_schemas.py::TestSchemas::test_interval
		"""

		with pytest.raises(exceptions.ValidationError, match="{'name': 'The \"name\" field is required.', 'params': 'The \"params\" field is required.'}"):
			schemas.interval.validate({})

		with pytest.raises(exceptions.ValidationError, match="{'name': 'Must be interval.', 'params': 'Must be an object.'}"):
			schemas.interval.validate({'name': 'foo', 'params': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'params': 'Must be an object.'}"):
			schemas.interval.validate({'name': 'interval', 'params': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'params': {'seconds': 'The \"seconds\" field is required.'}}"):
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


	def test_crontab_params(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_crontab_params
		"""

		with pytest.raises(exceptions.ValidationError, match="{'expression': 'The \"expression\" field is required.'}"):
			schemas.crontab_params.validate({})

		with pytest.raises(exceptions.ValidationError, match='Must be an object.'):
			schemas.crontab_params.validate({'foo'})

		with pytest.raises(exceptions.ValidationError, match="{'expression': 'The \"expression\" field is required.', 'foo': 'Invalid property name.'}"):
			schemas.crontab_params.validate({'foo': 'bar'})

		with pytest.raises(exceptions.ValidationError, match="{'expression': 'Must be a string.'}"):
			schemas.crontab_params.validate({'expression': 10})

		crontab_params = schemas.crontab_params.validate({'expression': '* * * * *'})
		assert crontab_params['expression'] == '* * * * *'


	def test_job(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_job
		"""

		with pytest.raises(exceptions.ValidationError, match="{'trigger': 'The \"trigger\" field is required.', 'task': 'The \"task\" field is required.'}"):
			schemas.Job({})

		with pytest.raises(exceptions.ValidationError, match="{'task': 'The \"task\" field is required.', 'trigger': 'Must match one of the union types.'}"):
			schemas.Job({'trigger': 'foo'})

		job = schemas.Job({'trigger': {'name': 'interval', 'params': {'seconds': 300}}, 'task': {'name': 'get', 'params': {'url': 'http://google.com'}}})
		assert job.trigger['name'] == 'interval'
		assert job.trigger['params'] == {'seconds': 300}
		assert job.trigger['params']['seconds'] == 300


	def test_schema(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_schema
		"""

		interval_params = {
			"seconds": 300
		}

		interval = {
			"name": "interval",
			"params": interval_params
		}

		log_params = {
			"message": "foo"
		}

		log = {
			"name": "log",
			"params": log_params
		}

		job = {
			"trigger": interval,
			"task": log
		}

		schemas.interval_params.validate(interval_params)
		schemas.interval.validate(interval)
		# schemas.log_params.validate(log_params)
		# schemas.log.validate(log)
		# schemas.Job.validate(job)


	def test_schemas(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_schemas
		"""

		path = '{}/schemas'.format(os.path.dirname(__file__))
		for file in os.listdir(path):

			with open('{}/{}'.format(path, file)) as f:

				if 'job-fail' in file:

					with pytest.raises((exceptions.ValidationError, KeyError)):
						schemas.Job.validate(json.load(f))

				elif 'job-pass' in file:
					assert schemas.Job.validate(json.load(f))

				else:
					print(file)
