import pytest
from src.exceptions.contact_type_exceptions import ContactTypeAlreadyExistsException, ContactTypeDatabaseException
from src.services.contact_type_service import create_contact_type, get_all_contact_types, get_contact_type_by_id, update_contact_type, delete_contact_type

def test_create_contact_type_service(app): 
    with app.app_context():
        contact_type_data = {'name': 'email', 'description': 'Personal email address'}
        contact_type = create_contact_type(contact_type_data)
        assert contact_type.name == 'email'
        assert contact_type.description == 'Personal email address'
        assert contact_type.id is not None

def test_create_contact_type_service_with_missing_description(app): 
    with app.app_context():
        contact_type_data = {'name': 'phone'}
        contact_type = create_contact_type(contact_type_data)
        assert contact_type.name == 'phone'
        assert contact_type.description is None
        assert contact_type.id is not None

def test_get_all_contact_types_service(app):
    with app.app_context():
        create_contact_type({'name': 'email', 'description': 'Personal email address'})
        create_contact_type({'name': 'phone'})
        contact_types = get_all_contact_types()
        assert len(contact_types) >= 2
        assert any(ct.name == 'email' for ct in contact_types)
        assert any(ct.name == 'phone' for ct in contact_types)

def test_get_contact_type_by_id_service(app):
    with app.app_context():
        contact_type_data = {'name': 'email', 'description': 'Personal email address'}
        contact_type = create_contact_type(contact_type_data)
        retrieved_contact_type = get_contact_type_by_id(contact_type.id)
        assert retrieved_contact_type.id == contact_type.id
        assert retrieved_contact_type.name == 'email'
        assert retrieved_contact_type.description == 'Personal email address'

def test_update_contact_type_service(app):
    with app.app_context():
        contact_type_data = {'name': 'email', 'description': 'Personal email address'}
        contact_type = create_contact_type(contact_type_data)

        # Update contact type using the service method
        update_data = {'name': 'work_email', 'description': 'Work email address'}
        updated_contact_type = update_contact_type(contact_type.id, update_data)

        assert updated_contact_type is not None
        assert updated_contact_type.name == 'work_email'
        assert updated_contact_type.description == 'Work email address'

def test_delete_contact_type_service(app):
    with app.app_context():
        contact_type_data = {'name': 'email', 'description': 'Personal email address'}
        contact_type = create_contact_type(contact_type_data)

        # Delete contact type using the service method
        deleted = delete_contact_type(contact_type.id)

        # Verify that the contact type is deleted
        deleted_contact_type = get_contact_type_by_id(contact_type.id)
        assert deleted_contact_type is None
        assert deleted is True