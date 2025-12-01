from flask_restful import Resource, Api
from flask import request
import logging

try:
    from models.user import User
    from schemas.user_schema import UserSchema
    from services.user_service import create_user, get_user, get_all_users, update_user, delete_user
    from exceptions.user_exceptions import UserException
    from utils.auth import jwt_required
except ImportError:
    from src.models.user import User
    from src.schemas.user_schema import UserSchema
    from src.services.user_service import create_user, get_user, get_all_users, update_user, delete_user
    from src.exceptions.user_exceptions import UserException
    from src.utils.auth import jwt_required

user_schema = UserSchema()
users_schema = UserSchema(many=True)

logger = logging.getLogger(__name__)

class UserResource(Resource):
    def get(self, user_id=None):
        logger.info(f"GET request for user(s), user_id: {user_id}")
        if user_id:
            user = get_user(user_id)
            if user:
                logger.info(f"User {user_id} found and returned")
                return user_schema.dump(user), 200
            logger.warning(f"User {user_id} not found")
            return {'message': 'User not found'}, 404
        else:
            users = get_all_users()
            logger.info(f"Returning {len(users)} users")
            return users_schema.dump(users), 200

    def post(self):
        try:
            logger.info("POST request to create user")
            user_data = request.get_json()
            logger.debug(f"User data received: {user_data}")
            user = create_user(user_data)
            logger.info(f"User created with ID: {user.id}")
            return user_schema.dump(user), 201
        except UserException as e:
            logger.error(f"User creation failed: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def put(self, user_id):
        try:
            logger.info(f"PUT request to update user {user_id}")
            user_data = request.get_json()
            logger.debug(f"Update data received: {user_data}")
            user = update_user(user_id, user_data)
            if user:
                logger.info(f"User {user_id} updated successfully")
                return user_schema.dump(user), 200
            logger.warning(f"User {user_id} not found for update")
            return {'message': 'User not found'}, 404
        except UserException as e:
            logger.error(f"User update failed: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def delete(self, user_id):
        logger.info(f"DELETE request for user {user_id}")
        if delete_user(user_id):
            logger.info(f"User {user_id} deleted successfully")
            return '', 204
        logger.warning(f"User {user_id} not found for deletion")
        return {'message': 'User not found'}, 404