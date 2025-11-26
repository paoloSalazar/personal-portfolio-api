import pytest
from src.models.user import User
from src.schemas.user_schema import UserSchema


def test_get_all_users(client):
    """Test creating and retrieving users"""
    # Create users via API
    post1 = client.post('/api/users', json={
        'name': 'User 1',
        'email': 'user1@example.com',
        'password': 'password1'
    })
    assert post1.status_code == 201, f"POST failed: {post1.data}"

    post2 = client.post('/api/users', json={
        'name': 'User 2',
        'email': 'user2@example.com',
        'password': 'password2'
    })
    assert post2.status_code == 201, f"POST failed: {post2.data}"

    # Get all users
    response = client.get('/api/users')
    assert response.status_code == 200, f"GET failed: {response.data}"
    assert len(response.json) == 2

def test_create_user(client):
    response = client.post('/api/users', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201, f"POST failed: {response.data}"
    assert 'id' in response.json
    assert 'name' in response.json
    assert 'email' in response.json