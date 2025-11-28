import pytest
from unittest.mock import patch
from src.resources.contact_type_resource import ContactTypeResource


# Unit tests for contact_type_resource methods
@patch('src.resources.contact_type_resource.contact_type_schema')
@patch('src.resources.contact_type_resource.create_contact_type')
@patch('src.resources.contact_type_resource.request')
def test_contact_type_resource_post(mock_request, mock_create_contact_type, mock_schema, app):
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
    mock_schema.dump.assert_called_once_with(mock_contact_type)