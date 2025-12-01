from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

def jwt_required(fn):
    """
    Decorator to require JWT authentication for a route.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            logger.info(f"Authenticated request from user ID: {current_user_id}")
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f"JWT authentication failed: {str(e)}")
            return jsonify({'error': 'Authentication required'}), 401
    return wrapper

def get_current_user_id():
    """
    Helper function to get the current user ID from JWT token.
    Assumes JWT has already been verified.
    """
    try:
        return get_jwt_identity()
    except Exception as e:
        logger.error(f"Failed to get current user ID: {str(e)}")
        return None