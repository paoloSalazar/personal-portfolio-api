try:
    from models.contact_type import ContactType
    from schemas.contact_type_schema import ContactTypeSchema
    from utils.extensions import db, bcrypt
    from exceptions.contact_type_exceptions import ContactTypeAlreadyExistsException, ContactTypeDatabaseException
except ImportError:
    from src.models.contact_type import ContactType
    from src.schemas.contact_type_schema import ContactTypeSchema
    from src.utils.extensions import db, bcrypt
    from src.exceptions.contact_type_exceptions import ContactTypeAlreadyExistsException, ContactTypeDatabaseException

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)
    
contact_type_schema = ContactTypeSchema()
contact_types_schema = ContactTypeSchema(many=True)

def create_contact_type(data):
    try:
        # Create contact type instance directly instead of using schema.load
        new_contact_type = ContactType(
            name=data['name'],
            description=data.get('description')
        )

        db.session.add(new_contact_type)
        db.session.commit()
        return new_contact_type
    except Exception as e:
        db.session.rollback()
        if "Duplicate entry" in str(e) and "name" in str(e):
            logger.error(f"Attempted to create contact type with duplicate name: {data['name']}")
            raise ContactTypeAlreadyExistsException(data['name'])
        else:
            logger.error(f"Database error during contact type creation: {str(e)}")
            raise ContactTypeDatabaseException(f"Failed to create contact type: {str(e)}")

def get_all_contact_types():
    return db.session.execute(select(ContactType)).scalars().all()

def get_contact_type_by_id(contact_type_id):
    return db.session.get(ContactType, contact_type_id)

def update_contact_type(contact_type_id, data):
    """
    Update a contact type.

    Behavior:
    - If 'name' is present in data => replace name.
    - If 'description' is present in data => replace description (can be None to clear).
    - If a key is omitted => leave that field unchanged.
    """
    contact_type = db.session.get(ContactType, contact_type_id)
    if contact_type:
        # Update fields only when provided in request payload
        if 'name' in data:
            contact_type.name = data['name']
        if 'description' in data:
            # use get so explicit None will set description to None
            contact_type.description = data.get('description')
        db.session.commit()
        return contact_type
    return None

def delete_contact_type(contact_type_id):
    contact_type = db.session.get(ContactType, contact_type_id)
    if contact_type:
        db.session.delete(contact_type)
        db.session.commit()
        return True
    return False