
import pytest
from unittest.mock import patch
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
