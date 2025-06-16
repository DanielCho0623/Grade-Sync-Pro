import pytest
<<<<<<< HEAD
<<<<<<< HEAD
from application import create_app, db
from application.models.user import User
=======
from app import create_app, db
from app.models.user import User
>>>>>>> 22c8b51 (backend deployment config and tests)
=======
from application import create_app, db
from application.models.user import User
>>>>>>> d3528df (rename app directory to application)

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_login(client):
<<<<<<< HEAD
<<<<<<< HEAD
=======
    # First register
>>>>>>> 22c8b51 (backend deployment config and tests)
=======
>>>>>>> 4990274 (clean up code)
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })

<<<<<<< HEAD
<<<<<<< HEAD
=======
    # Then login
>>>>>>> 22c8b51 (backend deployment config and tests)
=======
>>>>>>> 4990274 (clean up code)
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
