import pytest
import json


def test_user_registration_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'name': 'John',
        'last_name': 'Doe',
        'second_last_name': 'Smith',
        'email': 'john.doe@example.com',
        'password': 'securepassword123'
    })

    assert response.status_code == 201
    data = response.get_json()

    # Check response structure
    assert 'message' in data
    assert 'user' in data
    assert 'access_token' in data
    assert 'refresh_token' in data

    # Check user data
    user = data['user']
    assert user['name'] == 'John'
    assert user['last_name'] == 'Doe'
    assert user['email'] == 'john.doe@example.com'
    assert user['id'] is not None

    # Check tokens are strings
    assert isinstance(data['access_token'], str)
    assert isinstance(data['refresh_token'], str)


def test_user_registration_missing_fields(client):
    """Test registration with missing required fields"""
    # Missing email
    response = client.post('/api/auth/register', json={
        'name': 'John',
        'last_name': 'Doe',
        'password': 'securepassword123'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'email' in data['error']


def test_user_registration_duplicate_email(client):
    """Test registration with duplicate email"""
    # First registration
    client.post('/api/auth/register', json={
        'name': 'John',
        'last_name': 'Doe',
        'email': 'duplicate@example.com',
        'password': 'password123'
    })

    # Second registration with same email
    response = client.post('/api/auth/register', json={
        'name': 'Jane',
        'last_name': 'Smith',
        'email': 'duplicate@example.com',
        'password': 'password456'
    })

    assert response.status_code == 500
    data = response.get_json()
    print(data)
    assert 'error' in data


def test_user_login_success(client):
    """Test successful user login"""
    # First register a user
    client.post('/api/auth/register', json={
        'name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'password': 'mypassword123'
    })

    # Now login
    response = client.post('/api/auth/login', json={
        'email': 'jane.smith@example.com',
        'password': 'mypassword123'
    })

    assert response.status_code == 200
    data = response.get_json()

    # Check response structure
    assert 'message' in data
    assert 'user' in data
    assert 'access_token' in data
    assert 'refresh_token' in data

    # Check user data
    user = data['user']
    assert user['name'] == 'Jane'
    assert user['last_name'] == 'Smith'
    assert user['email'] == 'jane.smith@example.com'


def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    # Try to login without registering first
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid email or password' in data['error']


def test_user_login_missing_fields(client):
    """Test login with missing fields"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com'
        # Missing password
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_invalid_auth_action(client):
    """Test invalid auth action"""
    response = client.post('/api/auth/invalid_action', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid action' in data['error']


def test_register_and_login_integration(client):
    """Test complete registration and login flow"""
    # Register
    register_response = client.post('/api/auth/register', json={
        'name': 'Test',
        'last_name': 'User',
        'email': 'test.user@example.com',
        'password': 'testpass123'
    })

    assert register_response.status_code == 201
    register_data = register_response.get_json()
    original_user_id = register_data['user']['id']

    # Login with same credentials
    login_response = client.post('/api/auth/login', json={
        'email': 'test.user@example.com',
        'password': 'testpass123'
    })

    assert login_response.status_code == 200
    login_data = login_response.get_json()

    # Verify same user ID
    assert login_data['user']['id'] == original_user_id

    # Verify tokens are different (new login generates new tokens)
    assert login_data['access_token'] != register_data['access_token']
    assert login_data['refresh_token'] != register_data['refresh_token']