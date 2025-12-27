from flask import Blueprint

try:
    from resources.user_resource import UserResource, UploadPhotoResource
    from resources.contact_type_resource import ContactTypeResource
    from resources.auth_resource import AuthResource
    from resources.skill_resource import SkillResource
    from resources.user_skill_resource import UserSkillResource
    from resources.user_contact_resource import UserContactResource
    from resources.resume_resource import ResumeResource
    from resources.resume_skill_resource import ResumeSkillResource
except ImportError:
    from src.resources.user_resource import UserResource, UploadPhotoResource
    from src.resources.contact_type_resource import ContactTypeResource
    from src.resources.auth_resource import AuthResource
    from src.resources.skill_resource import SkillResource
    from src.resources.user_skill_resource import UserSkillResource
    from src.resources.user_contact_resource import UserContactResource
    from src.resources.resume_resource import ResumeResource
    from src.resources.resume_skill_resource import ResumeSkillResource

api_bp = Blueprint('api', __name__)

## User routes
api_bp.add_url_rule('/users', view_func=UserResource.as_view('users'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>', view_func=UserResource.as_view('user'), methods=['GET', 'PUT', 'DELETE'])
api_bp.add_url_rule('/users/<int:user_id>/upload-photo', view_func=UploadPhotoResource.as_view('upload_photo'), methods=['POST'])

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

# Resume routes
api_bp.add_url_rule('/users/<int:user_id>/resumes', view_func=ResumeResource.as_view('resumes'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>/resumes/<int:resume_id>', view_func=ResumeResource.as_view('resume'), methods=['GET', 'PUT', 'DELETE'])

# Resume Skill routes
api_bp.add_url_rule('/users/<int:user_id>/resumes/<int:resume_id>/skills', view_func=ResumeSkillResource.as_view('resume_skills'), methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>/resumes/<int:resume_id>/skills/<int:skill_id>', view_func=ResumeSkillResource.as_view('resume_skill'), methods=['DELETE'])