import pytest
import json
from src.services.user_service import create_user
from src.services.contact_type_service import create_contact_type
from src.services.user_contact_service import create_user_contact

def test_get_user_contacts(client, app):
    with app.app_context():
        # Create user and contact types
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        phone_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})
        email_type = create_contact_type({'name': 'Email', 'description': 'Email address'})

        # Create contacts
        create_user_contact({
            'user_id': user.id,
            'contacttype_id': phone_type.id,
            'link_or_number': '+1234567890'
        })
        create_user_contact({
            'user_id': user.id,
            'contacttype_id': email_type.id,
            'link_or_number': 'test@example.com'
        })

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Get user contacts
        response = client.get(f'/users/{user.id}/contacts', headers=headers)
        assert response.status_code == 200
        contacts = response.get_json()
        assert len(contacts) == 2
        contact_values = [c['link_or_number'] for c in contacts]
        assert '+1234567890' in contact_values
        assert 'test@example.com' in contact_values

def test_get_user_contact_by_id(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Create contact
        contact = create_user_contact({
            'user_id': user.id,
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        })

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Get specific contact
        response = client.get(f'/users/{user.id}/contacts/{contact.id}', headers=headers)
        assert response.status_code == 200
        contact_data = response.get_json()
        assert contact_data['value'] == '+1234567890'
        assert contact_data['user_id'] == user.id
        assert contact_data['contacttype_id'] == contact_type.id

def test_create_user_contact(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create contact
        response = client.post(f'/users/{user.id}/contacts', json={
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        }, headers=headers)
        assert response.status_code == 201
        contact_data = response.get_json()
        assert contact_data['value'] == '+1234567890'
        assert contact_data['user_id'] == user.id
        assert contact_data['contacttype_id'] == contact_type.id

def test_update_user_contact(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Create contact
        contact = create_user_contact({
            'user_id': user.id,
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        })

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Update contact
        response = client.put(f'/users/{user.id}/contacts/{contact.id}', json={
            'value': '+0987654321'
        }, headers=headers)
        assert response.status_code == 200
        contact_data = response.get_json()
        assert contact_data['value'] == '+0987654321'

def test_delete_user_contact(client, app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Create contact
        contact = create_user_contact({
            'user_id': user.id,
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        })

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Delete contact
        response = client.delete(f'/users/{user.id}/contacts/{contact.id}', headers=headers)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Contact deleted successfully'

def test_get_user_contacts_unauthorized(client, app):
    with app.app_context():
        # Create two users
        user1_data = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user2_data = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user1_data)
        user2 = create_user(user2_data)

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to access user2's contacts
        response = client.get(f'/users/{user2.id}/contacts', headers=headers)
        assert response.status_code == 403
        assert response.get_json()['error'] == 'Unauthorized to access this user\'s contacts'

def test_create_user_contact_unauthorized(client, app):
    with app.app_context():
        # Create two users and a contact type
        user1_data = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user2_data = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user1_data)
        user2 = create_user(user2_data)
        contact_type = create_contact_type({'name': 'Phone', 'description': 'Phone number'})

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to create contact for user2
        response = client.post(f'/users/{user2.id}/contacts', json={
            'contacttype_id': contact_type.id,
            'value': '+1234567890'
        }, headers=headers)
        assert response.status_code == 403
        assert response.get_json()['error'] == 'Unauthorized to modify this user\'s contacts'