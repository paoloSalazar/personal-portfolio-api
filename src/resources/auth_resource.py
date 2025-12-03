from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
import logging

try:
    from services.user_service import create_user, verify_password
    from exceptions.user_exceptions import UserException
except ImportError:
    from src.services.user_service import create_user, verify_password
    from src.exceptions.user_exceptions import UserException

logger = logging.getLogger(__name__)

class AuthResource(Resource):
    def post(self, action=None):
        if action == 'register':
            return self.register()
        elif action == 'login':
            return self.login()
        else:
            return {'error': 'Invalid action. Use /register or /login'}, 400

    def register(self):
        try:
            logger.info("POST request to register user")
            user_data = request.get_json()
            logger.debug(f"Registration data received: {user_data}")

            # Validate required fields
            required_fields = ['name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    return {'error': f'Missing required field: {field}'}, 400

            user = create_user(user_data)
            logger.info(f"User registered with ID: {user.id}")

            # Create tokens
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return {
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201

        except UserException as e:
            logger.error(f"Registration failed: {e.message}")
            return {'error': e.message}, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            return {'error': 'Internal server error'}, 500

    def login(self):
        try:
            logger.info("POST request to login user")
            login_data = request.get_json()
            logger.debug(f"Login data received: {login_data}")

            # Validate required fields
            if 'email' not in login_data or 'password' not in login_data:
                return {'error': 'Email and password are required'}, 400

            user = verify_password(login_data['email'], login_data['password'])
            if user:
                # Create tokens
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))

                logger.info(f"User {user.email} logged in successfully")
                return {
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'last_name': user.last_name,
                        'email': user.email
                    },
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            else:
                logger.warning(f"Failed login attempt for email: {login_data['email']}")
                return {'error': 'Invalid email or password'}, 401

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return {'error': 'Internal server error'}, 500