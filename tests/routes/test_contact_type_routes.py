import pytest
from src.models.contact_type import ContactType
from src.schemas.contact_type_schema import ContactTypeSchema
from src.services.user_service import create_user

def test_create_contact_type(client):
    # Create user and contact type
    user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
    user = create_user(user_data)

    # Login to get token
    login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    token = login_response.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
        
    response = client.post('/api/contacttypes', json={
        'name': 'email',
        'description': 'Personal email address',
    }, headers=headers)
    assert response.status_code == 201, f"POST failed: {response.data}"
    assert 'id' in response.json
    assert 'name' in response.json
    assert 'description' in response.json

def test_create_contact_type_with_missing_description(client):
    # Create user and contact type
    user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
    user = create_user(user_data)

    # Login to get token
    login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    token = login_response.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.post('/api/contacttypes', json={
        'name': 'phone',
    }, headers=headers)
    assert response.status_code == 201, f"POST failed: {response.data}"
    assert 'id' in response.json
    assert 'name' in response.json
    assert response.json.get('description') is None

def test_get_all_contact_types(client):
    """Test creating and retrieving contact types"""
    # Create user and contact type
    user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
    user = create_user(user_data)

    # Login to get token
    login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    token = login_response.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    
    # Create contact types via API
    post1 = client.post('/api/contacttypes', json={
        'name': 'email',
        'description': 'Personal email address',
    }, headers=headers)
    assert post1.status_code == 201, f"POST failed: {post1.data}"

    post2 = client.post('/api/contacttypes', json={
        'name': 'phone',
    }, headers=headers)
    assert post2.status_code == 201, f"POST failed: {post2.data}"

    # Get all contact types
    response = client.get('/api/contacttypes')
    assert response.status_code == 200, f"GET failed: {response.data}"
    assert len(response.json) == 2

def test_get_contact_type_by_id(client):
    # Create user and contact type
    user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
    user = create_user(user_data)

    # Login to get token
    login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    token = login_response.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a contact type via API
    post = client.post('/api/contacttypes', json={
        'name': 'email',
        'description': 'Personal email address',
    }, headers=headers)
    assert post.status_code == 201, f"POST failed: {post.data}"
    contact_type_id = post.json['id']

    # Get the contact type by ID
    response = client.get(f'/api/contacttypes/{contact_type_id}')
    assert response.status_code == 200, f"GET failed: {response.data}"
    assert response.json['id'] == contact_type_id
    assert response.json['name'] == 'email'
    assert response.json['description'] == 'Personal email address'

def test_update_contact_type(client):
    # Create user and contact type
    user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
    user = create_user(user_data)

    # Login to get token
    login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    token = login_response.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a contact type via API
    post = client.post('/api/contacttypes', json={
        'name': 'email',
        'description': 'Personal email address',
    }, headers=headers)
    assert post.status_code == 201, f"POST failed: {post.data}"
    contact_type_id = post.json['id']

    # Update the contact type via API
    put = client.put(f'/api/contacttypes/{contact_type_id}', json={
        'name': 'work_email',
        'description': 'Work email address',
    }, headers=headers)
    assert put.status_code == 200, f"PUT failed: {put.data}"
    assert put.json['id'] == contact_type_id
    assert put.json['name'] == 'work_email'
    assert put.json['description'] == 'Work email address'

def test_delete_contact_type(client):
    # Create user and contact type
    user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
    user = create_user(user_data)

    # Login to get token
    login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    token = login_response.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a contact type via API
    post = client.post('/api/contacttypes', json={
        'name': 'email',
        'description': 'Personal email address',
    }, headers=headers)
    assert post.status_code == 201, f"POST failed: {post.data}"
    contact_type_id = post.json['id']

    # Delete the contact type via API
    delete = client.delete(f'/api/contacttypes/{contact_type_id}', headers=headers)
    assert delete.status_code == 200, f"DELETE failed: {delete.data}"

    # Verify that the contact type is deleted
    get = client.get(f'/api/contacttypes/{contact_type_id}')
    assert get.status_code == 404, f"GET after DELETE should fail: {get.data}"