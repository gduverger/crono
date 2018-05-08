import app

from apistar.test import TestClient


client = TestClient(app)


def test_index():
    """
    Testing a view directly.
    """
    data = app.index()
    assert data == {'hello': 'world'}


def test_index_get():
    """
    Testing a view, using the test client.
    """
    response = client.get('http://localhost/') # http://127.0.0.1:8000 
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}
