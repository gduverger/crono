import pytest
import crono


"""
python -m pytest tests/test_api.py
"""


class TestApi(object):
	"""
	python -m pytest tests/test_api.py::TestApi
	"""


	def test_api(self):
		"""
		python -m pytest tests/test_api.py::TestApi::test_api
		"""

		job = crono.log('test')
		assert isinstance(job, crono.job.Job)
		assert job.task == 'crono.tasks.log'

		job.at('0 6 * * 2')
		assert isinstance(job, crono.job.Job)
