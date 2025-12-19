try:
    from models.user import User
    from models.contact_type import ContactType
    from models.user_contact import UserContact
    from services.user_service import get_user
    from services.contact_type_service import get_contact_type_by_id
    from utils.extensions import db
    from exceptions.user_contact_exceptions import UserContactException
except ImportError:
    from src.models.user import User
    from src.models.contact_type import ContactType
    from src.models.user_contact import UserContact
    from src.services.user_service import get_user
    from src.services.contact_type_service import get_contact_type_by_id
    from src.utils.extensions import db
    from src.exceptions.user_contact_exceptions import UserContactException

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

def create_user_contact(data):
    try:
        user = get_user(data['user_id'])
        if not user:
            raise UserContactException(f"User with id {data['user_id']} not found.", status_code=404)

        contact_type = get_contact_type_by_id(data['contacttype_id'])
        if not contact_type:
            raise UserContactException(f"Contact type with id {data['contacttype_id']} not found.", status_code=404)

        user_contact = UserContact(
            user_id=data['user_id'],
            contacttype_id=data['contacttype_id'],
            link_or_number=data['link_or_number']
        )

        db.session.add(user_contact)
        db.session.commit()
        return user_contact
    except Exception as e:
        db.session.rollback()
        if isinstance(e, UserContactException):
            raise
        logger.error(f"Database error during user contact creation: {str(e)}")
        raise UserContactException(f"Failed to create user contact: {str(e)}", status_code=500)

def get_user_contacts(user_id):
    try:
        user = get_user(user_id)
        if not user:
            raise UserContactException(f"User with id {user_id} not found.", status_code=404)

        return db.session.execute(
            select(UserContact).where(UserContact.user_id == user_id)
        ).scalars().all()
    except Exception as e:
        if isinstance(e, UserContactException):
            raise
        logger.error(f"Database error during getting user contacts: {str(e)}")
        raise UserContactException(f"Failed to get user contacts: {str(e)}", status_code=500)

def get_user_contact_by_id(user_contact_id):
    return db.session.get(UserContact, user_contact_id)

def update_user_contact(user_contact_id, data):
    try:
        user_contact = db.session.get(UserContact, user_contact_id)
        if not user_contact:
            raise UserContactException(f"User contact with id {user_contact_id} not found.", status_code=404)

        # Validate user if user_id is being updated
        if 'user_id' in data:
            user = get_user(data['user_id'])
            if not user:
                raise UserContactException(f"User with id {data['user_id']} not found.", status_code=404)
            user_contact.user_id = data['user_id']

        # Validate contact type if contacttype_id is being updated
        if 'contacttype_id' in data:
            contact_type = get_contact_type_by_id(data['contacttype_id'])
            if not contact_type:
                raise UserContactException(f"Contact type with id {data['contacttype_id']} not found.", status_code=404)
            user_contact.contacttype_id = data['contacttype_id']

        # Update link_or_number if provided
        if 'link_or_number' in data:
            user_contact.link_or_number = data['link_or_number']

        db.session.commit()
        return user_contact
    except Exception as e:
        db.session.rollback()
        if isinstance(e, UserContactException):
            raise
        logger.error(f"Database error during user contact update: {str(e)}")
        raise UserContactException(f"Failed to update user contact: {str(e)}", status_code=500)

def delete_user_contact(user_contact_id):
    try:
        user_contact = db.session.get(UserContact, user_contact_id)
        if not user_contact:
            raise UserContactException(f"User contact with id {user_contact_id} not found.", status_code=404)

        db.session.delete(user_contact)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        if isinstance(e, UserContactException):
            raise
        logger.error(f"Database error during user contact deletion: {str(e)}")
        raise UserContactException(f"Failed to delete user contact: {str(e)}", status_code=500)