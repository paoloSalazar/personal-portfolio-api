from flask_restful import Resource, Api
from flask import request
import logging

try:
    from models.skill import Skill
    from schemas.skill_schema import SkillSchema
    from services.skill_service import create_skill, get_all_skills, get_skill_by_id
    from exceptions.skill_exceptions import SkillException
    from utils.auth import jwt_required
except ImportError:
    from src.models.skill import Skill
    from src.schemas.skill_schema import SkillSchema
    from src.services.skill_service import create_skill, get_all_skills, get_skill_by_id
    from src.exceptions.skill_exceptions import SkillException
    from src.utils.auth import jwt_required

skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)

logger = logging.getLogger(__name__)

class SkillResource(Resource):
    def get(self, id=None):
        logger.info(f"GET request for contact type(s), id: {id}")
        if id:
            skill = get_skill_by_id(id)
            if skill:
                logger.info(f"Skill {id} found and returned")
                return skill_schema.dump(skill), 200
            logger.warning(f"Skill {id} not found")
            return {'message': 'Skill not found'}, 404
        else:
            skills = get_all_skills()
            logger.info(f"Returning {len(skills)} skills")
            return skills_schema.dump(skills), 200
    
    def post(self):
        try:
            logger.info("POST request to create skill")
            skill_data = request.get_json()
            logger.debug(f"Skill data received: {skill_data}")
            skill = create_skill(skill_data)
            logger.info(f"Skill created with ID: {skill.id}")
            return skill_schema.dump(skill), 201
        except SkillException as e:
            logger.error(f"Skill creation failed: {e.message}")
            return {'error': e.message}, e.status_code