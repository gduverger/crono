import pytest

from apistar import exceptions
from api import schemas


class TestSchemas(object):
	"""
	python -m pytest tests/test_schemas.py::TestSchemas
	"""


	def test_empty_job(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_empty_job
		"""

		with pytest.raises(exceptions.ValidationError, match=r'.*This field is required\..*'):
			job = schemas.Job({})


	def test_incomplete_job(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_incomplete_job
		"""

		job = schemas.Job({'trigger': {
			'name': 'interval',
			'params': {}
		}, 'task': {
			'name': 'log',
			'params': {}
		}})

		assert job.trigger['name'] == 'interval'
		assert job.trigger['params'] == {}
		assert job.task['name'] == 'log'
		assert job.task['params'] == {}


	def test_job(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_job
		"""

		job = {
			"trigger": {
				"name": "interval",
				"params": {
					"seconds": 10
				}
			},
			"task": {
				"name": "email",
				"params": {
					"to": "email@address.com",
					"subject": "Subject",
					"body": "Body"
				}
			}
		}

		j = schemas.Job(job)

		with pytest.raises(AttributeError):
			j.trigger.name

		assert j.trigger['name'] == 'interval'
		# assert j.trigger['params']['seconds'] == 10
		assert j.task['name'] == 'email'
		assert j.task['params']['to'] == 'email@address.com'
