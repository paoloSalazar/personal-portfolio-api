import pytest
from src.services.user_service import create_user
from src.services.contact_type_service import create_contact_type

def test_create_user_contact_route(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Login to get token
        login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create contact via API
        response = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': contact_type.id,
            'link_or_phone': '+1234567890'
        }, headers=headers)
        assert response.status_code == 201, f"POST failed: {response.data}"
        assert 'id' in response.json
        assert response.json['user_id'] == user.id
        assert response.json['contacttype_id'] == contact_type.id
        assert response.json['link_or_phone'] == '+1234567890'

def test_get_user_contacts_route(client, app):
    with app.app_context():
        # Create user and contact types
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        phone_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})
        email_type = create_contact_type({'name': 'Email', 'description': 'Email address'})

        # Login to get token
        login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create contacts via API
        post1 = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': phone_type.id,
            'value': '+1234567890'
        }, headers=headers)
        assert post1.status_code == 201, f"POST failed: {post1.data}"

        post2 = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': email_type.id,
            'value': 'test@example.com'
        }, headers=headers)
        assert post2.status_code == 201, f"POST failed: {post2.data}"

        # Get all contacts
        response = client.get(f'/users/{user.id}/contacts', headers=headers)
        assert response.status_code == 200, f"GET failed: {response.data}"
        assert len(response.json) == 2

def test_get_user_contact_by_id_route(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Login to get token
        login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create contact via API
        post_response = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        }, headers=headers)
        assert post_response.status_code == 201
        contact_id = post_response.json['id']

        # Get specific contact
        response = client.get(f'/users/{user.id}/contacts/{contact_id}', headers=headers)
        assert response.status_code == 200, f"GET failed: {response.data}"
        assert response.json['value'] == '+1234567890'
        assert response.json['id'] == contact_id

def test_update_user_contact_route(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Login to get token
        login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create contact via API
        post_response = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        }, headers=headers)
        assert post_response.status_code == 201
        contact_id = post_response.json['id']

        # Update contact
        response = client.put(f'/users/{user.id}/contacts/{contact_id}', json={
            'value': '+0987654321'
        }, headers=headers)
        assert response.status_code == 200, f"PUT failed: {response.data}"
        assert response.json['value'] == '+0987654321'

def test_delete_user_contact_route(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Login to get token
        login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create contact via API
        post_response = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        }, headers=headers)
        assert post_response.status_code == 201
        contact_id = post_response.json['id']

        # Delete contact
        response = client.delete(f'/users/{user.id}/contacts/{contact_id}', headers=headers)
        assert response.status_code == 200, f"DELETE failed: {response.data}"
        assert response.json['message'] == 'Contact deleted successfully'