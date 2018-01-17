import falcon
import pytest

from falcon import testing
from crono.app import api


@pytest.fixture
def client():
	return testing.TestClient(api)


def test_get(client):
	response = client.simulate_get('/jobs')
	# assert response.content == 'Jobs'
	assert response.status == falcon.HTTP_OK
