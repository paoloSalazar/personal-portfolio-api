from flask_restful import Resource, Api
from flask import request
import logging

try:
    from models.user import User
    from schemas.user_schema import UserSchema
    from services.user_service import create_user, get_user, get_all_users, update_user, delete_user
    from exceptions.user_exceptions import UserException
    from utils.auth import jwt_required, get_current_user_id
except ImportError:
    from src.models.user import User
    from src.schemas.user_schema import UserSchema
    from src.services.user_service import create_user, get_user, get_all_users, update_user, delete_user
    from src.exceptions.user_exceptions import UserException
    from src.utils.auth import jwt_required, get_current_user_id

# Import Supabase service only when needed to avoid initialization errors
def get_supabase_storage():
    try:
        from services.supabase_storage_service import get_supabase_storage as _get_storage
        return _get_storage()
    except ImportError:
        from src.services.supabase_storage_service import get_supabase_storage as _get_storage
        return _get_storage()

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

    @jwt_required
    def upload_photo(self, user_id):
        try:
            logger.info(f"POST request to upload profile photo for user {user_id}")

            # Check if user owns this profile
            current_user_id = get_current_user_id()
            if str(current_user_id) != str(user_id):
                logger.warning(f"User {current_user_id} attempted to upload photo for user {user_id}")
                return {'error': 'You can only upload photos to your own profile'}, 403

            # Check if photo file is provided
            if 'photo' not in request.files:
                return {'error': 'No photo file provided'}, 400

            file = request.files['photo']
            if not file or file.filename == '':
                return {'error': 'No photo file selected'}, 400

            # Upload to Supabase
            supabase_storage = get_supabase_storage()
            photo_url = supabase_storage.upload_profile_photo(file, user_id)

            # Update user record
            update_data = {'profile_photo_url': photo_url}
            updated_user = update_user(user_id, update_data)

            if not updated_user:
                return {'error': 'Failed to update user profile'}, 500

            logger.info(f"Profile photo uploaded successfully for user {user_id}")
            return {
                'message': 'Profile photo uploaded successfully',
                'profile_photo_url': photo_url,
                'user_id': user_id
            }, 200

        except ValueError as e:
            logger.error(f"Validation error during photo upload: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            logger.error(f"Unexpected error during photo upload: {str(e)}")
            return {'error': 'Failed to upload photo'}, 500