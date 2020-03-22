"""
python -m pytest tests/test_api.py
"""

import os
import datetime
import crono
import logging
import celery


class TestApi(object):
	"""
	python -m pytest tests/test_api.py::TestApi
	"""


	def test_request(self):
		"""
		python -m pytest tests/test_api.py::TestApi::test_request --capture=sys --log-cli-level=DEBUG
		"""

		json = {'text': 'every', 'token': os.getenv('PRINT_API_TOKEN')}
		job = crono.request('POST', 'https://print-gduverger.herokuapp.com/crono', json=json).every(minutes=1)


	def test_api(self):
		"""
		python -m pytest tests/test_api.py::TestApi::test_api --capture=sys --log-cli-level=DEBUG
		"""

		job = crono.log(logging.DEBUG, 'foo')
		assert isinstance(job, crono.job.Job)
		assert isinstance(job.task, str)
		assert job.task == 'crono.tasks.log'
		assert job.args == (logging.DEBUG, 'foo')
		assert job.kwargs == {}

		job = job.every(minutes=1)
		assert isinstance(job, crono.job.Job)
		assert isinstance(job.trigger, celery.schedules.schedule)

		job = crono.log(logging.DEBUG, 'bar').every(minutes=1)
		assert isinstance(job, crono.job.Job)
