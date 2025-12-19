import pytest
from src.services.user_contact_service import (
    create_user_contact, get_user_contacts, get_user_contact_by_id,
    update_user_contact, delete_user_contact
)
from src.services.user_service import create_user
from src.services.contact_type_service import create_contact_type

def test_create_user_contact_service(app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type_data = {'name': 'Phone', 'description': 'Phone number'}
        contact_type = create_contact_type(contact_type_data)

        contact_data = {
            'user_id': user.id,
            'contacttype_id': contact_type.id,
            'link_or_number': '+1234567890'
        }
        contact = create_user_contact(contact_data)
        assert contact.user_id == user.id
        assert contact.contacttype_id == contact_type.id
        assert contact.link_or_number == '+1234567890'
        assert contact.id is not None

def test_create_user_contact_invalid_user(app):
    with app.app_context():
        contact_type_data = {'name': 'Email', 'description': 'Email address'}
        contact_type = create_contact_type(contact_type_data)

        contact_data = {
            'user_id': 999,
            'contacttype_id': contact_type.id,
            'link_or_number': 'test@example.com'
        }
        with pytest.raises(Exception) as exc_info:
            create_user_contact(contact_data)
        assert exc_info.value.status_code == 404

def test_create_user_contact_invalid_contact_type(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        contact_data = {
            'user_id': user.id,
            'contacttype_id': 999,
            'link_or_number': 'test@example.com'
        }
        with pytest.raises(Exception) as exc_info:
            create_user_contact(contact_data)
        assert exc_info.value.status_code == 404

def test_get_user_contacts_service(app):
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

        contacts = get_user_contacts(user.id)
        assert len(contacts) == 2
        contact_values = [c.link_or_number for c in contacts]
        assert '+1234567890' in contact_values
        assert 'test@example.com' in contact_values

def test_get_user_contacts_invalid_user(app):
    with app.app_context():
        with pytest.raises(Exception) as exc_info:
            get_user_contacts(999)
        assert exc_info.value.status_code == 404

def test_update_user_contact_service(app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type_data = {'name': 'Phone', 'description': 'Phone number'}
        contact_type = create_contact_type(contact_type_data)

        contact_data = {
            'user_id': user.id,
            'contacttype_id': contact_type.id,
            'link_or_number': '+1234567890'
        }
        contact = create_user_contact(contact_data)

        # Update contact
        update_data = {'link_or_number': '+0987654321'}
        updated_contact = update_user_contact(contact.id, update_data)
        assert updated_contact.link_or_number == '+0987654321'
        assert updated_contact.id == contact.id

def test_update_user_contact_invalid_id(app):
    with app.app_context():
        update_data = {'value': 'newvalue@example.com'}
        with pytest.raises(Exception) as exc_info:
            update_user_contact(999, update_data)
        assert exc_info.value.status_code == 404

def test_delete_user_contact_service(app):
    with app.app_context():
        # Create user and contact type
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        contact_type_data = {'name': 'Phone', 'description': 'Phone number'}
        contact_type = create_contact_type(contact_type_data)

        contact_data = {
            'user_id': user.id,
            'contacttype_id': contact_type.id,
            'link_or_number': '+1234567890'
        }
        contact = create_user_contact(contact_data)

        # Delete contact
        result = delete_user_contact(contact.id)
        assert result is True

        # Verify contact is deleted
        deleted_contact = get_user_contact_by_id(contact.id)
        assert deleted_contact is None

def test_delete_user_contact_invalid_id(app):
    with app.app_context():
        with pytest.raises(Exception) as exc_info:
            delete_user_contact(999)
        assert exc_info.value.status_code == 404