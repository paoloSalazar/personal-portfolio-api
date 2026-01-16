import pytest
from src.models.contact_type import ContactType


def test_contact_type_init():
    """Test ContactType initialization."""
    contact_type = ContactType(name="Email", description="Email contact type")
    assert contact_type.id == None
    assert contact_type.name == "Email"
    assert contact_type.description == "Email contact type"

def test_contact_type_repr():
    """Test ContactType __repr__ method."""
    contact_type = ContactType(name="Phone", description="Phone contact type")
    assert repr(contact_type) == '<ContactType Phone Phone contact type>'

def test_contact_type_attributes():
    """Test ContactType has required attributes."""
    contact_type = ContactType(name="LinkedIn", description="LinkedIn contact type")
    assert hasattr(contact_type, 'id')
    assert hasattr(contact_type, 'name')
    assert hasattr(contact_type, 'description')
    assert hasattr(contact_type, 'created_at')
    assert hasattr(contact_type, 'updated_at')

