import pytest
from unittest.mock import patch, MagicMock
from src.resources.auth_resource import AuthResource


# Unit tests for auth_resource methods
@patch('src.resources.auth_resource.create_access_token')
@patch('src.resources.auth_resource.create_refresh_token')
@patch('src.resources.auth_resource.create_user')
@patch('src.resources.auth_resource.request')
def test_auth_resource_register_success(mock_request, mock_create_user, mock_create_refresh_token, mock_create_access_token):
    """Test successful user registration"""
    # Mock request data
    mock_request.get_json.return_value = {
        'name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    }

    # Mock created user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.name = 'John'
    mock_user.last_name = 'Doe'
    mock_user.email = 'john@example.com'
    mock_create_user.return_value = mock_user

    # Mock tokens
    mock_create_access_token.return_value = 'access_token_123'
    mock_create_refresh_token.return_value = 'refresh_token_456'

    # Test the register method
    resource = AuthResource()
    result, status = resource.register()

    # Assertions
    assert status == 201
    assert result['message'] == 'User registered successfully'
    assert result['user']['id'] == 1
    assert result['user']['name'] == 'John'
    assert result['user']['email'] == 'john@example.com'
    assert result['access_token'] == 'access_token_123'
    assert result['refresh_token'] == 'refresh_token_456'

    mock_create_user.assert_called_once_with({
        'name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })


@patch('src.resources.auth_resource.create_user')
@patch('src.resources.auth_resource.request')
def test_auth_resource_register_missing_field(mock_request, mock_create_user):
    """Test registration with missing required field"""
    # Mock request data with missing email
    mock_request.get_json.return_value = {
        'name': 'John',
        'last_name': 'Doe',
        'password': 'password123'
        # Missing email
    }

    # Test the register method
    resource = AuthResource()
    result, status = resource.register()

    # Assertions
    assert status == 400
    assert 'error' in result
    assert 'email' in result['error']
    mock_create_user.assert_not_called()


@patch('src.resources.auth_resource.create_access_token')
@patch('src.resources.auth_resource.create_refresh_token')
@patch('src.resources.auth_resource.verify_password')
@patch('src.resources.auth_resource.request')
def test_auth_resource_login_success(mock_request, mock_verify_password, mock_create_refresh_token, mock_create_access_token):
    """Test successful user login"""
    # Mock request data
    mock_request.get_json.return_value = {
        'email': 'john@example.com',
        'password': 'password123'
    }

    # Mock verified user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.name = 'John'
    mock_user.last_name = 'Doe'
    mock_user.email = 'john@example.com'
    mock_verify_password.return_value = mock_user

    # Mock tokens
    mock_create_access_token.return_value = 'access_token_789'
    mock_create_refresh_token.return_value = 'refresh_token_101'

    # Test the login method
    resource = AuthResource()
    result, status = resource.login()

    # Assertions
    assert status == 200
    assert result['message'] == 'Login successful'
    assert result['user']['id'] == 1
    assert result['user']['name'] == 'John'
    assert result['access_token'] == 'access_token_789'
    assert result['refresh_token'] == 'refresh_token_101'

    mock_verify_password.assert_called_once_with('john@example.com', 'password123')


@patch('src.resources.auth_resource.verify_password')
@patch('src.resources.auth_resource.request')
def test_auth_resource_login_invalid_credentials(mock_request, mock_verify_password):
    """Test login with invalid credentials"""
    # Mock request data
    mock_request.get_json.return_value = {
        'email': 'john@example.com',
        'password': 'wrongpassword'
    }

    # Mock verify_password returning None (invalid credentials)
    mock_verify_password.return_value = None

    # Test the login method
    resource = AuthResource()
    result, status = resource.login()

    # Assertions
    assert status == 401
    assert 'error' in result
    assert 'Invalid email or password' in result['error']


@patch('src.resources.auth_resource.request')
def test_auth_resource_login_missing_password(mock_request):
    """Test login with missing password"""
    # Mock request data with missing password
    mock_request.get_json.return_value = {
        'email': 'john@example.com'
        # Missing password
    }

    # Test the login method
    resource = AuthResource()
    result, status = resource.login()

    # Assertions
    assert status == 400
    assert 'error' in result


@patch('src.resources.auth_resource.request')
def test_auth_resource_post_invalid_action(mock_request):
    """Test POST with invalid action"""
    # Mock request data
    mock_request.get_json.return_value = {
        'email': 'test@example.com',
        'password': 'password123'
    }

    # Test the post method with invalid action
    resource = AuthResource()
    result, status = resource.post('invalid_action')

    # Assertions
    assert status == 400
    assert 'error' in result
    assert 'Invalid action' in result['error']


@patch('src.resources.auth_resource.create_access_token')
@patch('src.resources.auth_resource.create_refresh_token')
@patch('src.resources.auth_resource.create_user')
@patch('src.resources.auth_resource.request')
def test_auth_resource_register_with_second_last_name(mock_request, mock_create_user, mock_create_refresh_token, mock_create_access_token):
    """Test registration with optional second_last_name field"""
    # Mock request data including second_last_name
    mock_request.get_json.return_value = {
        'name': 'John',
        'last_name': 'Doe',
        'second_last_name': 'Smith',
        'email': 'john.smith@example.com',
        'password': 'password123'
    }

    # Mock created user
    mock_user = MagicMock()
    mock_user.id = 2
    mock_user.name = 'John'
    mock_user.last_name = 'Doe'
    mock_user.second_last_name = 'Smith'
    mock_user.email = 'john.smith@example.com'
    mock_create_user.return_value = mock_user

    # Mock tokens
    mock_create_access_token.return_value = 'access_token_xyz'
    mock_create_refresh_token.return_value = 'refresh_token_abc'

    # Test the register method
    resource = AuthResource()
    result, status = resource.register()

    # Assertions
    assert status == 201
    assert result['user']['second_last_name'] == 'Smith'

    # Verify create_user was called with second_last_name
    call_args = mock_create_user.call_args[0][0]
    assert call_args['second_last_name'] == 'Smith'