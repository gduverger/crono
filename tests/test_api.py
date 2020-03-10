import crono
import logging


"""
python -m pytest tests/test_api.py
"""


class TestApi(object):
	"""
	python -m pytest tests/test_api.py::TestApi
	"""


	def test_api(self):
		"""
		python -m pytest tests/test_api.py::TestApi::test_api --capture=sys --log-cli-level=DEBUG
		"""

		job = crono.log('TEST!!!!!!!!!!!!!!!!!!!')
		assert isinstance(job, crono.job.Job)
		assert job.task == 'crono.tasks.log'

		job = job.in_(minutes=7)
		assert isinstance(job, crono.job.Job)
