import json
import falcon
import pytest

from falcon import testing
from api.main import api


@pytest.fixture
def client():
	return testing.TestClient(api)


def test_jobs_get(client):
	response = client.simulate_get('/jobs')
	assert response.status == falcon.HTTP_OK
	assert 'job_ids' in json.loads(response.content)


def test_jobs_post(client):
	response = client.simulate_post('/jobs')
	assert response.status == falcon.HTTP_CREATED
	assert 'job_id' in json.loads(response.content)


def test_job_get(client):
	response = client.simulate_get('/jobs/1')
	assert response.status == falcon.HTTP_OK
	assert 'job_id' in json.loads(response.content)
