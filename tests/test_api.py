"""
python -m pytest tests/test_api.py
"""

import os
import datetime
import crono
import logging
import celery

from crono.job import Job

class TestApi(object):
	"""
	python -m pytest tests/test_api.py::TestApi
	"""

	def test_api(self):
		"""
		python -m pytest tests/test_api.py::TestApi::test_api --capture=sys --log-cli-level=DEBUG
		"""

		job = crono.log(logging.DEBUG, 'foo')
		assert isinstance(job, Job)
		assert isinstance(job.task, str)
		assert job.task == 'crono.tasks.log'
		assert job.args == (logging.DEBUG, 'foo')
		assert job.kwargs == {}

		job = job.every(minutes=1)
		assert isinstance(job, Job)
		assert isinstance(job.trigger, celery.schedules.schedule)

		job = crono.log(logging.DEBUG, 'bar').every(minutes=1)
		assert isinstance(job, Job)
