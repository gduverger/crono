from api import app
from apistar.test import TestClient

"""
python -m pytest
"""

client = TestClient(app.app)

def test_index():
	data = app.index()
	assert data == 'crono'


def test_index_get():
	response = client.get('/')
	assert response.status_code == 200
	assert response.text == 'crono'
