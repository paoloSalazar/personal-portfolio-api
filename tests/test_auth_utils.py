import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.utils.auth import jwt_required, get_current_user_id


@pytest.fixture
def app():
    """Create a test Flask app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    return app


def test_get_current_user_id_success(app):
    """Test get_current_user_id with valid JWT"""
    with app.app_context():
        with patch('src.utils.auth.get_jwt_identity') as mock_get_jwt:
            mock_get_jwt.return_value = 123

            result = get_current_user_id()
            assert result == 123
            mock_get_jwt.assert_called_once()


def test_get_current_user_id_failure(app):
    """Test get_current_user_id with JWT error"""
    with app.app_context():
        with patch('src.utils.auth.get_jwt_identity') as mock_get_jwt:
            mock_get_jwt.side_effect = Exception('JWT Error')

            result = get_current_user_id()
            assert result is None


@patch('src.utils.auth.verify_jwt_in_request')
@patch('src.utils.auth.get_jwt_identity')
def test_jwt_required_success(mock_get_jwt, mock_verify, app):
    """Test jwt_required decorator with valid token"""
    with app.app_context():
        mock_verify.return_value = None  # verify_jwt_in_request doesn't return anything
        mock_get_jwt.return_value = 456

        @jwt_required
        def test_function():
            return {'success': True}

        result = test_function()
        assert result == {'success': True}
        mock_verify.assert_called_once()
        mock_get_jwt.assert_called_once()


# @patch('src.utils.auth.verify_jwt_in_request')
# def test_jwt_required_failure(mock_verify, app):
#     """Test jwt_required decorator with invalid token"""
#     with app.app_context():
#         mock_verify.side_effect = Exception('Invalid token')

#         @jwt_required
#         def test_function():
#             return {'success': True}

#         result, status = test_function()
#         assert status == 401
#         assert 'error' in result
#         assert 'Authentication required' in result['error']
#         mock_verify.assert_called_once()


@patch('src.utils.auth.verify_jwt_in_request')
@patch('src.utils.auth.get_jwt_identity')
def test_jwt_required_with_args_kwargs(mock_get_jwt, mock_verify, app):
    """Test jwt_required decorator preserves function arguments"""
    with app.app_context():
        mock_verify.return_value = None
        mock_get_jwt.return_value = 789

        @jwt_required
        def test_function_with_args(user_id, action=None):
            return {'user_id': user_id, 'action': action}

        result = test_function_with_args(123, action='update')
        assert result == {'user_id': 123, 'action': 'update'}
        mock_verify.assert_called_once()
        mock_get_jwt.assert_called_once()


@patch('src.utils.auth.verify_jwt_in_request')
@patch('src.utils.auth.get_jwt_identity')
@patch('src.utils.auth.logger')
def test_jwt_required_logging(mock_logger, mock_get_jwt, mock_verify, app):
    """Test that jwt_required logs authenticated requests"""
    with app.app_context():
        mock_verify.return_value = None
        mock_get_jwt.return_value = 999

        @jwt_required
        def test_function():
            return {'data': 'test'}

        result = test_function()

        # Verify logging was called
        mock_logger.info.assert_called_once_with("Authenticated request from user ID: 999")

        # Verify function still works
        assert result == {'data': 'test'}