import pytest
from src.models.user_contact import UserContact


def test_user_contact_init():
    """Test UserContact initialization."""
    user_contact = UserContact(user_id=1, contacttype_id=2, link_or_number='http://example.com')
    assert user_contact.user_id == 1
    assert user_contact.contacttype_id == 2
    assert user_contact.link_or_number == 'http://example.com'

def test_user_contact_repr():
    """Test UserContact __repr__ method."""
    user_contact = UserContact(user_id=1, contacttype_id=2, link_or_number='http://example.com')
    expected_repr = '<UserContact user_id=1 contacttype_id=2 value=http://example.com>'
    assert repr(user_contact) == expected_repr


def test_user_contact_attributes():
    """Test UserContact attributes."""
    user_contact = UserContact(user_id=3, contacttype_id=4, link_or_number='123-456-7890')
    assert hasattr(user_contact, 'id')
    assert hasattr(user_contact, 'user_id')
    assert hasattr(user_contact, 'contacttype_id')
    assert hasattr(user_contact, 'link_or_number')
    assert hasattr(user_contact, 'created_at')
    assert hasattr(user_contact, 'updated_at')