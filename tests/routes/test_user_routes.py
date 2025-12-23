import pytest
from unittest.mock import patch
from io import BytesIO
from src.models.user import User
from src.schemas.user_schema import UserSchema


def test_get_all_users(client):
    """Test creating and retrieving users"""
    # Create users via API
    post1 = client.post('/api/users', json={
        'name': 'User 1',
        'last_name': 'Last1',
        'second_last_name': 'Second1',
        'email': 'user1@example.com',
        'password': 'password1',
        'about_me': 'About user 1'
    })
    assert post1.status_code == 201, f"POST failed: {post1.data}"

    post2 = client.post('/api/users', json={
        'name': 'User 2',
        'last_name': 'Last2',
        'second_last_name': 'Second2',
        'email': 'user2@example.com',
        'password': 'password2',
        'about_me': 'About user 2'
    })
    assert post2.status_code == 201, f"POST failed: {post2.data}"

    # Get all users
    response = client.get('/api/users')
    assert response.status_code == 200, f"GET failed: {response.data}"
    assert len(response.json) == 2

def test_create_user(client):
    response = client.post('/api/users', json={
        'name': 'John Doe',
        'last_name': 'Doe',
        'second_last_name': 'Jr',
        'email': 'john@example.com',
        'password': 'password123',
        'about_me': 'I am John Doe',
        'profile_photo_url': 'https://example.com/photo.jpg'
    })
    assert response.status_code == 201, f"POST failed: {response.data}"
    assert 'id' in response.json
    assert 'name' in response.json
    assert 'last_name' in response.json
    assert 'second_last_name' in response.json
    assert 'email' in response.json
    assert 'about_me' in response.json
    assert 'profile_photo_url' in response.json
    assert response.json['about_me'] == 'I am John Doe'
    assert response.json['profile_photo_url'] == 'https://example.com/photo.jpg'


def test_upload_profile_photo_route(client, app):
    with app.app_context():
        # Create user
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        from src.services.user_service import create_user
        user = create_user(user_data)

        # Login to get token
        login_response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Mock the supabase upload
        with patch('src.services.supabase_storage_service.get_supabase_storage') as mock_get_storage:
            mock_storage = mock_get_storage.return_value
            mock_storage.upload_profile_photo.return_value = 'https://example.com/uploaded-photo.jpg'

            # Create a test file
            test_file = BytesIO(b'fake image data')
            test_file.filename = 'test.jpg'

            # Upload photo
            response = client.post(
                f'/api/users/{user.id}/upload-photo',
                data={'photo': (test_file, 'test.jpg')},
                content_type='multipart/form-data',
                headers=headers
            )

            assert response.status_code == 200, f"POST failed: {response.data}"
            assert 'message' in response.json
            assert 'profile_photo_url' in response.json
            assert 'user_id' in response.json
            assert response.json['profile_photo_url'] == 'https://example.com/uploaded-photo.jpg'
            assert response.json['user_id'] == user.id
            assert response.json['message'] == 'Profile photo uploaded successfully'

            # Verify the upload was called
            mock_storage.upload_profile_photo.assert_called_once()