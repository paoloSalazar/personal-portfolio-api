from flask_restful import Resource
from flask import request
import logging

try:
    from schemas.skill_schema import SkillSchema
    from services.resume_skill_service import assign_skills_to_resume, remove_skill_from_resume, get_resume_skills
    from utils.auth import jwt_required, get_current_user_id
except ImportError:
    from src.schemas.skill_schema import SkillSchema
    from src.services.resume_skill_service import assign_skills_to_resume, remove_skill_from_resume, get_resume_skills
    from src.utils.auth import jwt_required, get_current_user_id

skills_schema = SkillSchema(many=True)

logger = logging.getLogger(__name__)

class ResumeSkillResource(Resource):

    # @jwt_required
    def get(self, user_id, resume_id):
        # current_user_id = str(get_current_user_id())
        # if str(user_id) != current_user_id:
        #     logger.warning(f"User {current_user_id} attempted to access skills for resume of user {user_id}")
        #     return {'error': 'Unauthorized to access this user\'s resume skills'}, 403

        try:
            skills = get_resume_skills(resume_id)
            logger.info(f"Returning {len(skills)} skills for resume {resume_id}")
            return skills_schema.dump(skills), 200
        except ValueError as e:
            logger.error(f"Failed to get resume skills: {e}")
            return {'error': str(e)}, 400

    @jwt_required
    def post(self, user_id, resume_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to assign skills to resume of user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s resume skills'}, 403

        try:
            data = request.get_json()
            skill_ids = data.get('skill_ids')
            if not skill_ids or not isinstance(skill_ids, list):
                return {'error': 'skill_ids must be a non-empty list'}, 400
            result = assign_skills_to_resume(resume_id, skill_ids)
            assigned_count = len(result['assigned'])
            logger.info(f"{assigned_count} skills assigned to resume {resume_id}")
            response = {'message': f'Skills assigned successfully', 'assigned_count': assigned_count}
            if result['errors']:
                response['errors'] = result['errors']
            return response, 201
        except ValueError as e:
            logger.error(f"Skills assignment to resume failed: {e}")
            return {'error': str(e)}, 400

    @jwt_required
    def delete(self, user_id, resume_id, skill_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to remove skill from resume of user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s resume skills'}, 403

        try:
            remove_skill_from_resume(resume_id, skill_id)
            logger.info(f"Skill {skill_id} removed from resume {resume_id}")
            return {'message': 'Skill removed successfully'}, 200
        except ValueError as e:
            logger.error(f"Skill removal from resume failed: {e}")
            return {'error': str(e)}, 400