import pytest
from src.models.user import User
from src.schemas.user_schema import UserSchema

def test_create_user(client):
    response = client.post('/api/users', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert 'name' in response.json
    assert 'email' in response.json
    assert 'password' in response.json  # Password is now returned

def test_get_user(client):
    # First create a user
    client.post('/api/users', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'skills': ['Python', 'Flask']
    })
    response = client.get('/api/users/1')
    assert response.status_code == 200
    assert 'name' in response.json

def test_update_user(client):
    # First create a user
    client.post('/api/users', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    response = client.put('/api/users/1', json={
        'name': 'John Doe Updated',
        'email': 'john_updated@example.com',
        'password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe Updated'
    assert response.json['email'] == 'john_updated@example.com'

def test_delete_user(client):
    # First create a user
    client.post('/api/users', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    response = client.delete('/api/users/1')
    assert response.status_code == 204

def test_get_nonexistent_user(client):
    response = client.get('/api/users/999')
    assert response.status_code == 404

def test_get_all_users(client):
    # Create a couple of users
    client.post('/api/users', json={
        'name': 'User 1',
        'email': 'user1@example.com',
        'password': 'password1'
    })
    client.post('/api/users', json={
        'name': 'User 2',
        'email': 'user2@example.com',
        'password': 'password2'
    })
    response = client.get('/api/users')
    assert response.status_code == 200
    assert len(response.json) == 2
    # Check that passwords are returned
    for user in response.json:
        assert 'password' in user