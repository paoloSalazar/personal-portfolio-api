from flask_restful import Resource, Api
from flask import request
import logging

try:
    from models.contact_type import ContactType
    from schemas.contact_type_schema import ContactTypeSchema
    from services.contact_type_service import create_contact_type, get_all_contact_types, get_contact_type_by_id
    from exceptions.contact_type_exceptions import ContactTypeException
except ImportError:
    from src.models.contact_type import ContactType
    from src.schemas.contact_type_schema import ContactTypeSchema
    from src.services.contact_type_service import create_contact_type, get_all_contact_types, get_contact_type_by_id
    from src.exceptions.contact_type_exceptions import ContactTypeException

contact_type_schema = ContactTypeSchema()
contact_types_schema = ContactTypeSchema(many=True)

logger = logging.getLogger(__name__)

class ContactTypeResource(Resource):
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