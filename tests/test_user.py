import pytest
from src.models.user import User
from src.schemas.user_schema import UserSchema



# def test_get_user(client):
#     # First create a user
#     client.post('/api/users', json={
#         'name': 'Test User',
#         'email': 'test@example.com',
#         'skills': ['Python', 'Flask']
#     })
#     response = client.get('/api/users/1')
#     assert response.status_code == 200
#     assert 'name' in response.json

# def test_update_user(client):
#     # First create a user
#     client.post('/api/users', json={
#         'name': 'John Doe',
#         'email': 'john@example.com',
#         'password': 'password123'
#     })
#     response = client.put('/api/users/1', json={
#         'name': 'John Doe Updated',
#         'email': 'john_updated@example.com',
#         'password': 'newpassword123'
#     })
#     assert response.status_code == 200
#     assert response.json['name'] == 'John Doe Updated'
#     assert response.json['email'] == 'john_updated@example.com'

# def test_delete_user(client):
#     # First create a user
#     client.post('/api/users', json={
#         'name': 'John Doe',
#         'email': 'john@example.com',
#         'password': 'password123'
#     })
#     response = client.delete('/api/users/1')
#     assert response.status_code == 204

# def test_get_nonexistent_user(client):
#     response = client.get('/api/users/999')
#     assert response.status_code == 404

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
