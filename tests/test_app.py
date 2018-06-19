import os
import base64

from api import app, auth
from apistar.test import TestClient

"""
python -m pytest tests/test_app.py
"""

client = TestClient(app.app)


def test_jobs_not_authenticated():
	response = client.get('/jobs')
	assert response.status_code == 403
	assert response.text == '"Not authenticated"'


def test_jobs_authenticated():
	token = base64.b64encode(os.getenv('USER_TOKEN').encode('utf-8')).decode('utf-8')
	response = client.get('/test', auth=auth.HTTPBearerAuth(token))
	assert response.status_code == 200
