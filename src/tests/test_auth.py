import time
from fastapi.testclient import TestClient

from main import app
from database import get_db
from fixtures import override_get_db, setup_database


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register(setup_database):
    data = {
        'username': 'renren-017',
        'password': 'secretpass123'
    }

    start = time.time()
    response = client.post('/auth/register/', json=data)
    end = time.time()

    assert response.status_code == 200
    assert response.json() == data
    assert start-end < 0.001


def test_register_invalid_password(setup_database):
    data = {
        'username': 'renren-017',
        'password': 'secret'
    }

    start = time.time()
    response = client.post('/auth/register/', json=data)
    end = time.time()

    assert response.status_code == 422
    assert start - end < 0.001


def test_register_username_already_exists(setup_database):
    data = {
        'username': 'renren-017',
        'password': 'secret12345'
    }

    start = time.time()
    response = client.post('/auth/register/', json=data)
    end = time.time()

    assert response.status_code == 409
    assert start - end < 0.001


def test_token_obtain(setup_database):
    data = {
        'username': 'renren-017',
        'password': 'secretpass123'
    }

    start = time.time()
    response = client.post('/auth/token-obtain/', json=data)
    end = time.time()

    assert response.status_code == 200
    assert start - end < 0.001


def test_token_obtain_invalid_credentials(setup_database):
    data = {
        'username': 'nonexistent',
        'password': 'secretpass123'
    }

    start = time.time()
    response = client.post('/auth/token-obtain/', json=data)
    end = time.time()

    assert response.status_code == 401
    assert start - end < 0.001
