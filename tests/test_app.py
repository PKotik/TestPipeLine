import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200

def test_add_note(client):
    """Тест добавления заметки"""
    response = client.post('/notes', json={'note': 'Test note'})
    assert response.status_code == 201

def test_fetch_url(client):
    """Тест загрузки URL"""
    response = client.get('/fetch?url=https://example.com')
    assert response.status_code == 200