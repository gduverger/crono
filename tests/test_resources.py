import json
import falcon
import pytest

from falcon import testing
from api.main import api, TEST_TOKEN


HEADERS = {'Authorization': 'Bearer {}'.format(TEST_TOKEN)}


@pytest.fixture
def client():
	return testing.TestClient(api)


def test_jobs_get(client):
	response = client.simulate_get('/v0/jobs', headers=HEADERS)
	assert response.status == falcon.HTTP_OK
	assert type(json.loads(response.content)) is list


def test_jobs_post(client):
	params = {'command': 'log', 'trigger': 'interval', 'seconds': 60, 'text': 'test'}
	response = client.simulate_post('/v0/jobs', headers=HEADERS, params=params)
	content = json.loads(response.content)
	assert response.status == falcon.HTTP_CREATED
	assert type(content) is dict
	assert type(content['job']) is dict
	# assert content['job']['command'] == 'log' # <function lo... 0x106934a60>
	# assert content['job']['trigger'] == 'interval' # <IntervalTri...a/New_York')>
	assert content['job']['args'] == ['test']


def test_job_get(client):
	response = client.simulate_get('/v0/jobs/not-found', headers=HEADERS)
	assert response.status == falcon.HTTP_NOT_FOUND
