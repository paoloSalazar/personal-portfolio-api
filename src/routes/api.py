from flask import Blueprint
from resources.user_resource import UserResource

api_bp = Blueprint('api', __name__)

api_bp.add_url_rule('/users', view_func=UserResource.as_view('users'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>', view_func=UserResource.as_view('user'), methods=['GET', 'PUT', 'DELETE'])