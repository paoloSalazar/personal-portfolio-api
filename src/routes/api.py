from flask import Blueprint

try:
    from resources.user_resource import UserResource
    from resources.contact_type_resource import ContactTypeResource
except ImportError:
    from src.resources.user_resource import UserResource
    from src.resources.contact_type_resource import ContactTypeResource

api_bp = Blueprint('api', __name__)

## User routes
api_bp.add_url_rule('/users', view_func=UserResource.as_view('users'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>', view_func=UserResource.as_view('user'), methods=['GET', 'PUT', 'DELETE'])

# ContactType routes
api_bp.add_url_rule('/contacttypes', view_func=ContactTypeResource.as_view('contacttypes'), methods=['GET', 'POST'])
api_bp.add_url_rule('/contacttypes/<int:id>', view_func=ContactTypeResource.as_view('contacttype'), methods=['GET'])
