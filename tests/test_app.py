import os
import base64

from api import app, auth
from apistar.test import TestClient


"""
python -m pytest tests/test_app.py
"""


client = TestClient(app.app)


def test_jobs_not_authenticated():
	"""
	python -m pytest tests/test_app.py::test_jobs_not_authenticated
	"""
	response = client.get('/jobs')
	assert response.status_code == 403
	assert response.text == '"Not authenticated"'


def test_jobs_authenticated():
	"""
	python -m pytest tests/test_app.py::test_jobs_authenticated
	"""
	response = client.get('/jobs', auth=auth.HTTPBearerAuth(os.getenv('CRONO_API_TOKEN')))
	assert response.status_code == 200
