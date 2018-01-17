import json
import falcon
import pytest

from falcon import testing
from crono.app import api


@pytest.fixture
def client():
	return testing.TestClient(api)


def test_tests_get(client):
	response = client.simulate_get('/tests')
	assert json.loads(response.content) == {'test': True}
	assert response.status == falcon.HTTP_OK
