import os
import json
import pytest

from apistar import exceptions
from api import models


"""
python -m pytest tests/test_models.py
"""


class TestJob(object):
	"""
	python -m pytest tests/test_models.py::TestJob
	"""


	def test_job(self):
		"""
		python -m pytest tests/test_models.py::TestJob::test_job
		"""

		job = models.Job()
		assert isinstance(job.key, str)
		assert job.is_active == False
		assert job.record_id == None


	def test_job_to_dict(self):
		"""
		python -m pytest tests/test_models.py::TestJob::test_job_to_dict
		"""

		dict_ = models.Job().to_dict()
		assert 'key' in dict_
		assert isinstance(dict_['key'], str)


class TestUser(object):
	"""
	python -m pytest tests/test_models.py::TestUser
	"""


	@classmethod 
	def setup_class(cls):
		cls.user = models.User.get(os.getenv('CRONO_API_TOKEN_TEST'))
		cls.data = {
			"trigger": {
				"name": "crontab",
				"params": {
					"expression": "* * * * *"
				}
			},
			"task": {
				"name": "log",
				"params": {
					"message": "test"
				}
			}
		}


	def test_user(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user
		"""

		with pytest.raises(TypeError, message="__init__() missing 1 required positional argument: 'email'"):
			models.User()

		user = models.User('email')
		assert isinstance(user.email, str)
		assert user.email == 'email'
		assert isinstance(user.token, str)
		assert isinstance(user.is_active, bool)
		assert user.is_active == True
		assert user.jobs == None
		assert user.record_id == None


	def test_user_to_dict(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user_to_dict
		"""

		dict_ = models.User('email').to_dict()
		assert 'email' in dict_
		assert isinstance(dict_['email'], str)
		assert 'token' in dict_
		assert isinstance(dict_['token'], str)


	def test_user_get_job(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user_get_job
		"""

		job1 = models.Job(is_active=True)
		job2 = models.Job(is_active=True)
		job3 = models.Job(is_active=True, key=job1.key)
		user = models.User('email', jobs=[job1, job2, job3])

		assert user.get_job(job1.key) == job1
		assert user.get_job(job1.key) != job2
		assert user.get_job(job1.key) != job3


	@pytest.mark.skipif(os.getenv('ENVIRONMENT') == 'CI', reason='requires redis')
	def test_user_add_job(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user_add_job
		"""

		for i in range(0, 50):
			self.user.add_job(self.data)


	@pytest.mark.skipif(os.getenv('ENVIRONMENT') == 'CI', reason='requires redis')
	def test_user_remove_job(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user_remove_job
		"""

		job1 = self.user.add_job(self.data)
		assert job1.is_active == True
		job2 = self.user.remove_job(key=job1.key)
		assert job2.is_active == False
		assert job1 == job2


	@pytest.mark.skipif(os.getenv('ENVIRONMENT') == 'CI', reason='requires redis')
	def test_user_remove_jobs(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user_remove_jobs
		"""

		jobs = self.user.get_jobs(activity=[True, False])
		assert jobs == self.user.remove_jobs(activity=[True, False])


class TestLog(object):
	"""
	python -m pytest tests/test_models.py::TestLog
	"""


	def test_log(self):
		"""
		python -m pytest tests/test_models.py::TestLog::test_log
		"""

		# TODO
		pass
