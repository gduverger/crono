from api import schemas

"""
python -m pytest tests/test_schemas.py::TestSchemas
"""

class TestSchemas(object):


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
					"value": "georges.duverger@gmail"
				}]
			}
		}
		j = schemas.Job(job)
		assert j.trigger['name'] == 'interval'
