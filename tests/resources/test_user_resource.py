
import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from src.resources.user_resource import UserResource


# Unit tests for user_resource methods
@patch('src.resources.user_resource.users_schema')
@patch('src.resources.user_resource.get_all_users')
def test_user_resource_get_all(mock_get_all, mock_schema, app):
    mock_users = [{'name': 'User1', 'last_name': 'Last1', 'second_last_name': 'Second1', 'email': 'user1@example.com'}]
    mock_get_all.return_value = mock_users
    mock_schema.dump.return_value = mock_users

    resource = UserResource()
    result, status = resource.get()
    assert status == 200
    assert result == mock_users
    mock_get_all.assert_called_once()
    mock_schema.dump.assert_called_once_with(mock_users)

@patch('src.resources.user_resource.user_schema')
@patch('src.resources.user_resource.create_user')
@patch('src.resources.user_resource.request')
def test_user_resource_post(mock_request, mock_create_user, mock_schema, app):
    mock_request.get_json.return_value = {'name': 'New User', 'last_name': 'New Last', 'second_last_name': 'New Second', 'email': 'new@example.com', 'password': 'newpass', 'about_me': 'About new user'}
    mock_user = type('MockUser', (), {'name': 'New User', 'last_name': 'New Last', 'second_last_name': 'New Second', 'email': 'new@example.com', 'about_me': 'About new user'})()
    mock_create_user.return_value = mock_user
    mock_schema.dump.return_value = {'name': 'New User', 'last_name': 'New Last', 'second_last_name': 'New Second', 'email': 'new@example.com', 'about_me': 'About new user'}

    resource = UserResource()
    result, status = resource.post()
    assert status == 201
    assert result['name'] == 'New User'
    assert result['last_name'] == 'New Last'
    assert result['about_me'] == 'About new user'
    mock_create_user.assert_called_once_with({'name': 'New User', 'last_name': 'New Last', 'second_last_name': 'New Second', 'email': 'new@example.com', 'password': 'newpass', 'about_me': 'About new user'})
    mock_schema.dump.assert_called_once_with(mock_user)

@patch('src.resources.user_resource.user_schema')
@patch('src.resources.user_resource.get_user')
def test_user_resource_get_single(mock_get_user, mock_schema, app):
    mock_user = type('MockUser', (), {'name': 'Single User', 'last_name': 'Single Last', 'second_last_name': 'Single Second', 'email': 'single@example.com'})()
    mock_get_user.return_value = mock_user
    mock_schema.dump.return_value = {'name': 'Single User', 'last_name': 'Single Last', 'second_last_name': 'Single Second', 'email': 'single@example.com'}

    resource = UserResource()
    result, status = resource.get(1)
    assert status == 200
    assert result['name'] == 'Single User'
    assert result['last_name'] == 'Single Last'
    mock_get_user.assert_called_once_with(1)
    mock_schema.dump.assert_called_once_with(mock_user)


@patch('src.resources.user_resource.user_schema')
@patch('src.resources.user_resource.create_user')
@patch('src.resources.user_resource.update_user')
@patch('src.resources.user_resource.get_supabase_storage')
@patch('src.resources.user_resource.request')
def test_user_resource_post_with_photo(mock_request, mock_get_storage, mock_update_user, mock_create_user, mock_schema, app):
    # Mock multipart request
    mock_request.content_type = 'multipart/form-data'
    mock_request.form.get.return_value = '{"name": "New User", "last_name": "New Last", "second_last_name": "New Second", "email": "new@example.com", "password": "newpass"}'

    # Mock file
    mock_file = MagicMock()
    mock_file.filename = 'test.jpg'
    mock_request.files = {'photo': mock_file}

    # Mock user creation
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.profile_photo_url = None
    mock_create_user.return_value = mock_user

    # Mock storage service
    mock_storage = MagicMock()
    mock_storage.upload_profile_photo.return_value = 'https://example.com/photo.jpg'
    mock_get_storage.return_value = mock_storage

    # Mock update user
    mock_updated_user = MagicMock()
    mock_updated_user.profile_photo_url = 'https://example.com/photo.jpg'
    mock_update_user.return_value = mock_updated_user

    mock_schema.dump.return_value = {'name': 'New User', 'profile_photo_url': 'https://example.com/photo.jpg'}

    resource = UserResource()
    result, status = resource.post()

    assert status == 201
    assert result['profile_photo_url'] == 'https://example.com/photo.jpg'
    mock_create_user.assert_called_once()
    mock_storage.upload_profile_photo.assert_called_once_with(mock_file, 1)
    mock_update_user.assert_called_once_with(1, {'profile_photo_url': 'https://example.com/photo.jpg'})


@patch('src.resources.user_resource.user_schema')
@patch('src.resources.user_resource.create_user')
@patch('src.resources.user_resource.get_supabase_storage')
@patch('src.resources.user_resource.request')
def test_user_resource_post_with_photo_upload_fails(mock_request, mock_get_storage, mock_create_user, mock_schema, app):
    # Mock multipart request
    mock_request.content_type = 'multipart/form-data'
    mock_request.form.get.return_value = '{"name": "New User", "last_name": "New Last", "email": "new@example.com", "password": "newpass"}'

    # Mock file
    mock_file = MagicMock()
    mock_file.filename = 'test.jpg'
    mock_request.files = {'photo': mock_file}

    # Mock user creation
    mock_user = MagicMock()
    mock_user.id = 1
    mock_create_user.return_value = mock_user

    # Mock storage service to raise exception
    mock_storage = MagicMock()
    mock_storage.upload_profile_photo.side_effect = Exception("Upload failed")
    mock_get_storage.return_value = mock_storage

    mock_schema.dump.return_value = {'name': 'New User'}

    resource = UserResource()
    result, status = resource.post()

    assert status == 201  # User creation succeeds even if photo upload fails
    assert result['name'] == 'New User'
    mock_create_user.assert_called_once()
    mock_storage.upload_profile_photo.assert_called_once_with(mock_file, 1)


@patch('src.resources.user_resource.jwt_required')
@patch('src.resources.user_resource.get_current_user_id')
@patch('src.resources.user_resource.update_user')
@patch('src.resources.user_resource.get_supabase_storage')
@patch('src.resources.user_resource.request')
def test_user_resource_upload_photo(mock_request, mock_get_storage, mock_update_user, mock_get_current_user_id, mock_jwt_required, app):
    # Mock request
    mock_file = MagicMock()
    mock_file.filename = 'test.jpg'
    mock_request.files = {'photo': mock_file}

    # Mock current user
    mock_get_current_user_id.return_value = 1

    # Mock storage service
    mock_storage = MagicMock()
    mock_storage.upload_profile_photo.return_value = 'https://example.com/photo.jpg'
    mock_get_storage.return_value = mock_storage

    # Mock update user
    mock_updated_user = MagicMock()
    mock_update_user.return_value = mock_updated_user

    resource = UserResource()
    result, status = resource.upload_photo(1)

    assert status == 200
    assert result['profile_photo_url'] == 'https://example.com/photo.jpg'
    assert result['user_id'] == 1
    mock_storage.upload_profile_photo.assert_called_once_with(mock_file, 1)
    mock_update_user.assert_called_once_with(1, {'profile_photo_url': 'https://example.com/photo.jpg'})


@patch('src.resources.user_resource.jwt_required')
@patch('src.resources.user_resource.get_current_user_id')
@patch('src.resources.user_resource.request')
def test_user_resource_upload_photo_unauthorized(mock_request, mock_get_current_user_id, mock_jwt_required, app):
    # Mock current user trying to upload to different user
    mock_get_current_user_id.return_value = 1

    resource = UserResource()
    result, status = resource.upload_photo(2)

    assert status == 403
    assert result['error'] == 'You can only upload photos to your own profile'


@patch('src.resources.user_resource.jwt_required')
@patch('src.resources.user_resource.request')
def test_user_resource_upload_photo_no_file(mock_request, mock_jwt_required, app):
    mock_request.files = {}

    resource = UserResource()
    result, status = resource.upload_photo(1)

    assert status == 400
    assert result['error'] == 'No photo file provided'
