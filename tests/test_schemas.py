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


	def test_job(self):
		"""
		python -m pytest tests/test_schemas.py::TestSchemas::test_job
		"""

		job = {
			"trigger": {
				"name": "interval",
				"arg": 10
			},
			"command": {
				"name": "email",
				"args": [{
					"key": "to",
					"value": "email@address.com"
				}]
			}
		}

		j = schemas.Job(job)
		assert j.trigger['name'] == 'interval'
		assert j.trigger['arg'] == 10
		assert j.command['name'] == 'email'
		assert j.command['args'][0]['key'] == 'to'
		assert j.command['args'][0]['value'] == 'email@address.com'
