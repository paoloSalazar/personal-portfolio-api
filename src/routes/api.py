from flask import Blueprint

try:
    from resources.user_resource import UserResource
    from resources.contact_type_resource import ContactTypeResource
    from resources.auth_resource import AuthResource
    from resources.skill_resource import SkillResource
    from resources.user_skill_resource import UserSkillResource
    from resources.user_contact_resource import UserContactResource
except ImportError:
    from src.resources.user_resource import UserResource
    from src.resources.contact_type_resource import ContactTypeResource
    from src.resources.auth_resource import AuthResource
    from src.resources.skill_resource import SkillResource
    from src.resources.user_skill_resource import UserSkillResource
    from src.resources.user_contact_resource import UserContactResource

api_bp = Blueprint('api', __name__)

## User routes
api_bp.add_url_rule('/users', view_func=UserResource.as_view('users'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>', view_func=UserResource.as_view('user'), methods=['GET', 'PUT', 'DELETE'])

# Auth routes
api_bp.add_url_rule('/auth/<action>', view_func=AuthResource.as_view('auth'), methods=['POST'])

# ContactType routes
api_bp.add_url_rule('/contacttypes', view_func=ContactTypeResource.as_view('contacttypes'), methods=['GET', 'POST'])
api_bp.add_url_rule('/contacttypes/<int:id>', view_func=ContactTypeResource.as_view('contacttype'), methods=['GET','PUT', 'DELETE'])

# Skill routes
api_bp.add_url_rule('/skills', view_func=SkillResource.as_view('skills'), methods=['GET','POST'])
api_bp.add_url_rule('/skills/<int:id>', view_func=SkillResource.as_view('skill'), methods=['GET','PUT', 'DELETE'])

# User Skill routes
api_bp.add_url_rule('/users/<int:user_id>/skills', view_func=UserSkillResource.as_view('user_skills'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>/skills/<int:skill_id>', view_func=UserSkillResource.as_view('user_skill'), methods=['DELETE'])

# User Contact routes
api_bp.add_url_rule('/users/<int:user_id>/contacts', view_func=UserContactResource.as_view('user_contacts'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>/contacts/<int:contact_id>', view_func=UserContactResource.as_view('user_contact'), methods=['GET', 'PUT', 'DELETE'])