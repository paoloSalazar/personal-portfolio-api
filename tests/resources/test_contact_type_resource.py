import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from src.resources.contact_type_resource import ContactTypeResource


# Unit tests for contact_type_resource methods
@patch('src.utils.auth.get_jwt_identity')
@patch('src.utils.auth.verify_jwt_in_request')
@patch('src.resources.contact_type_resource.contact_type_schema')
@patch('src.resources.contact_type_resource.create_contact_type')
@patch('src.resources.contact_type_resource.request')
def test_contact_type_resource_post(mock_request, mock_create_contact_type, mock_schema, mock_verify_jwt, mock_get_jwt_identity, app):
    # Mock request data
    mock_request.get_json.return_value = {
        'name': 'email',
        'description': 'Personal email address'
    }

    # Mock created contact type
    mock_contact_type = type('MockContactType', (), {
        'id': 1,
        'name': 'email',
        'description': 'Personal email address'
    })()
    mock_create_contact_type.return_value = mock_contact_type

    # Mock schema dump
    mock_schema.dump.return_value = {
        'id': 1,
        'name': 'email',
        'description': 'Personal email address'
    }

    # Create JWT token for authorization
    with app.app_context():
        access_token = create_access_token(identity=1)
        mock_request.headers = {'Authorization': f'Bearer {access_token}'}

    # Mock JWT identity
    mock_get_jwt_identity.return_value = 1

    # Test the POST method
    resource = ContactTypeResource()
    result, status = resource.post()

    # Assertions
    assert status == 201
    assert result['name'] == 'email'
    assert result['description'] == 'Personal email address'
    mock_create_contact_type.assert_called_once_with({
        'name': 'email',
        'description': 'Personal email address'
    })
    # mock_schema.dump.assert_called_once_with(mock_contact_type)