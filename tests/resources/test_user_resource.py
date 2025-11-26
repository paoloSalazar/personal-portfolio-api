
import pytest
from unittest.mock import patch
from src.resources.user_resource import UserResource


# Unit tests for user_resource methods
@patch('src.resources.user_resource.users_schema')
@patch('src.resources.user_resource.get_all_users')
def test_user_resource_get_all(mock_get_all, mock_schema, app):
    mock_users = [{'name': 'User1', 'email': 'user1@example.com'}]
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
    mock_request.get_json.return_value = {'name': 'New User', 'email': 'new@example.com', 'password': 'newpass'}
    mock_user = type('MockUser', (), {'name': 'New User', 'email': 'new@example.com'})()
    mock_create_user.return_value = mock_user
    mock_schema.dump.return_value = {'name': 'New User', 'email': 'new@example.com'}

    resource = UserResource()
    result, status = resource.post()
    assert status == 201
    assert result['name'] == 'New User'
    mock_create_user.assert_called_once_with({'name': 'New User', 'email': 'new@example.com', 'password': 'newpass'})
    mock_schema.dump.assert_called_once_with(mock_user)

