from flask_restful import Resource
from flask import request
import logging

try:
    from schemas.user_contact_schema import UserContactSchema
    from services.user_contact_service import (
        create_user_contact, get_user_contacts, get_user_contact_by_id,
        update_user_contact, delete_user_contact
    )
    from exceptions.user_contact_exceptions import UserContactException
    from utils.auth import jwt_required, get_current_user_id
except ImportError:
    from src.schemas.user_contact_schema import UserContactSchema
    from src.services.user_contact_service import (
        create_user_contact, get_user_contacts, get_user_contact_by_id,
        update_user_contact, delete_user_contact
    )
    from src.exceptions.user_contact_exceptions import UserContactException
    from src.utils.auth import jwt_required, get_current_user_id

user_contact_schema = UserContactSchema()
user_contacts_schema = UserContactSchema(many=True)

logger = logging.getLogger(__name__)

class UserContactResource(Resource):
    @jwt_required
    def get(self, user_id, contact_id=None):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to access contacts of user {user_id}")
            return {'error': 'Unauthorized to access this user\'s contacts'}, 403

        logger.info(f"GET request for user {user_id} contacts, contact_id: {contact_id}")
        try:
            if contact_id:
                contact = get_user_contact_by_id(contact_id)
                if not contact or contact.user_id != user_id:
                    return {'error': 'Contact not found'}, 404
                logger.info(f"Contact {contact_id} found and returned")
                return user_contact_schema.dump(contact), 200
            else:
                contacts = get_user_contacts(user_id)
                logger.info(f"Returning {len(contacts)} contacts for user {user_id}")
                return user_contacts_schema.dump(contacts), 200
        except UserContactException as e:
            logger.error(f"Failed to get user contacts: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def post(self, user_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to create contact for user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s contacts'}, 403

        try:
            logger.info(f"POST request to create contact for user {user_id}")
            data = request.get_json()
            data['user_id'] = user_id  # Ensure user_id is set correctly
            contact = create_user_contact(data)
            logger.info(f"Contact created with ID: {contact.id}")
            return user_contact_schema.dump(contact), 201
        except UserContactException as e:
            logger.error(f"Contact creation failed: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def put(self, user_id, contact_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to update contact for user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s contacts'}, 403

        try:
            logger.info(f"PUT request to update contact {contact_id} for user {user_id}")
            data = request.get_json()
            contact = update_user_contact(contact_id, data)
            logger.info(f"Contact {contact_id} updated")
            return user_contact_schema.dump(contact), 200
        except UserContactException as e:
            logger.error(f"Contact update failed: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def delete(self, user_id, contact_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to delete contact for user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s contacts'}, 403

        try:
            logger.info(f"DELETE request to remove contact {contact_id} from user {user_id}")
            delete_user_contact(contact_id)
            logger.info(f"Contact {contact_id} deleted")
            return {'message': 'Contact deleted successfully'}, 200
        except UserContactException as e:
            logger.error(f"Contact deletion failed: {e.message}")
            return {'error': e.message}, e.status_code