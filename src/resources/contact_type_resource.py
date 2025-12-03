from flask_restful import Resource, Api
from flask import request
import logging

try:
    from models.contact_type import ContactType
    from schemas.contact_type_schema import ContactTypeSchema
    from services.contact_type_service import create_contact_type, get_all_contact_types, get_contact_type_by_id, update_contact_type, delete_contact_type
    from exceptions.contact_type_exceptions import ContactTypeException, ContactTypeNotFoundException
    from utils.auth import jwt_required
except ImportError:
    from src.models.contact_type import ContactType
    from src.schemas.contact_type_schema import ContactTypeSchema
    from src.services.contact_type_service import create_contact_type, get_all_contact_types, get_contact_type_by_id, update_contact_type, delete_contact_type
    from src.exceptions.contact_type_exceptions import ContactTypeException, ContactTypeNotFoundException
    from src.utils.auth import jwt_required

contact_type_schema = ContactTypeSchema()
contact_types_schema = ContactTypeSchema(many=True)

logger = logging.getLogger(__name__)

class ContactTypeResource(Resource):
    @jwt_required
    def post(self):
        try:
            logger.info("POST request to create contact type")
            contact_type_data = request.get_json()
            logger.debug(f"Contact Type data received: {contact_type_data}")
            contact_type = create_contact_type(contact_type_data)
            logger.info(f"Contact Type created with ID: {contact_type.id}")
            return contact_type_schema.dump(contact_type), 201
        except ContactTypeException as e:
            logger.error(f"Contact Type creation failed: {e.message}")
            return {'error': e.message}, e.status_code
        
    def get(self, id=None):
        logger.info(f"GET request for contact type(s), id: {id}")
        if id:
            contact_type = get_contact_type_by_id(id)
            if contact_type:
                logger.info(f"Contact Type {id} found and returned")
                return contact_type_schema.dump(contact_type), 200
            logger.warning(f"Contact Type {id} not found")
            return {'message': 'Contact Type not found'}, 404
        else:
            contact_types = get_all_contact_types()
            logger.info(f"Returning {len(contact_types)} contact types")
            return contact_types_schema.dump(contact_types), 200
        
    def put(self, id):
        try:
            logger.info(f"PUT request to update contact type {id}")
            contact_type_data = request.get_json()
            logger.debug(f"Update data received: {contact_type_data}")
            contact_type = update_contact_type(id, contact_type_data)
            if contact_type:
                logger.info(f"Contact Type {id} updated successfully")
                return contact_type_schema.dump(contact_type), 200
            logger.warning(f"Contact Type {id} not found for update")
            return {'message': 'Contact Type not found'}, 404
        except ContactTypeException as e:
            logger.error(f"Contact Type update failed: {e.message}")
            return {'error': e.message}, e.status_code
        
    def delete(self, id):  # Added delete method
        try:
            logger.info(f"DELETE request for contact type {id}")
            contact_type = get_contact_type_by_id(id)
            if contact_type:
                delete_contact_type(id)
                logger.info(f"Contact Type {id} deleted successfully")
                return {'message': 'Contact Type deleted successfully'}, 200
            logger.warning(f"Contact Type {id} not found for deletion")
            return {'message': f'Contact Type with ID {id} not found'}, 404
        except ContactTypeException as e:
            logger.error(f"Contact Type deletion failed: {e.message}")
            return {'error': e.message}, e.status_code