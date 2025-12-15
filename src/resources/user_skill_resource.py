from flask_restful import Resource
from flask import request
import logging

try:
    from schemas.skill_schema import SkillSchema
    from services.user_skill_service import assign_skill_to_user, remove_skill_from_user, get_user_skills
    from exceptions.skill_exceptions import SkillException
    from utils.auth import jwt_required, get_current_user_id
except ImportError:
    from src.schemas.skill_schema import SkillSchema
    from src.services.user_skill_service import assign_skill_to_user, remove_skill_from_user, get_user_skills
    from src.exceptions.skill_exceptions import SkillException
    from src.utils.auth import jwt_required, get_current_user_id

skills_schema = SkillSchema(many=True)

logger = logging.getLogger(__name__)

class UserSkillResource(Resource):
    @jwt_required
    def get(self, user_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to access skills of user {user_id}")
            return {'error': 'Unauthorized to access this user\'s skills'}, 403

        logger.info(f"GET request for user {user_id} skills")
        try:
            skills = get_user_skills(user_id)
            logger.info(f"Returning {len(skills)} skills for user {user_id}")
            return skills_schema.dump(skills), 200
        except SkillException as e:
            logger.error(f"Failed to get user skills: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def post(self, user_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to assign skill to user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s skills'}, 403

        try:
            logger.info(f"POST request to assign skill to user {user_id}")
            data = request.get_json()
            skill_id = data.get('skill_id')
            if not skill_id:
                return {'error': 'skill_id is required'}, 400
            user_skill = assign_skill_to_user(user_id, skill_id)
            logger.info(f"Skill {skill_id} assigned to user {user_id}")
            return {'message': 'Skill assigned successfully'}, 201
        except SkillException as e:
            logger.error(f"Skill assignment failed: {e.message}")
            return {'error': e.message}, e.status_code

    @jwt_required
    def delete(self, user_id, skill_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to remove skill from user {user_id}")
            return {'error': 'Unauthorized to modify this user\'s skills'}, 403

        try:
            logger.info(f"DELETE request to remove skill {skill_id} from user {user_id}")
            remove_skill_from_user(user_id, skill_id)
            logger.info(f"Skill {skill_id} removed from user {user_id}")
            return {'message': 'Skill removed successfully'}, 200
        except SkillException as e:
            logger.error(f"Skill removal failed: {e.message}")
            return {'error': e.message}, e.status_code