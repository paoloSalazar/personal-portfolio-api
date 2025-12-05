try:
    from models.skill import Skill
    from schemas.skill_schema import SkillSchema
    from utils.extensions import db, bcrypt
    from exceptions.skill_exceptions import SkillException
except ImportError:
    from src.models.skill import Skill
    from src.schemas.skill_schema import SkillSchema
    from src.utils.extensions import db, bcrypt
    from src.exceptions.skill_exceptions import SkillException

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)
    
skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)

def create_skill(data):
    try:
        # Create skill instance directly instead of using schema.load
        new_skill = Skill(
            name=data['name'],
            description=data['description']
        )

        db.session.add(new_skill)
        db.session.commit()
        return new_skill
    except Exception as e:
        db.session.rollback()
        if "Duplicate entry" in str(e) and "name" in str(e):
            logger.error(f"Attempted to create skill with duplicate name: {data['name']}")
            raise SkillException(f"Skill with name {data['name']} already exists.", status_code=400)
        else:
            logger.error(f"Database error during skill creation: {str(e)}")
            raise SkillException(f"Failed to create skill: {str(e)}", status_code=500)

def get_all_skills():
    return db.session.execute(select(Skill)).scalars().all()

def get_skill_by_id(skill_id):
    return db.session.get(Skill, skill_id)