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
		assert job.is_active == True
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
		assert isinstance(user.balance, int)
		assert user.balance == 1
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
		assert 'balance' in dict_
		assert isinstance(dict_['balance'], int)


	def test_user_get_job(self):
		"""
		python -m pytest tests/test_models.py::TestUser::test_user_get_job
		"""

		job = models.Job()
		job2 = models.Job()
		job3 = models.Job(key=job.key)
		user = models.User('email', jobs=[job, job2, job3])

		assert user.get_job(job.key) == job
		assert user.get_job(job.key) != job2
		assert user.get_job(job.key) != job3
