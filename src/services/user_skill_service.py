try:
    from models.user import User
    from models.skill import Skill
    from models.user_skill import UserSkill
    from services.user_service import get_user
    from services.skill_service import get_skill_by_id
    from utils.extensions import db
    from exceptions.skill_exceptions import SkillException
except ImportError:
    from src.models.user import User
    from src.models.skill import Skill
    from src.models.user_skill import UserSkill
    from src.services.user_service import get_user
    from src.services.skill_service import get_skill_by_id
    from src.utils.extensions import db
    from src.exceptions.skill_exceptions import SkillException

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

def assign_skill_to_user(user_id, skill_id):
    try:
        user = get_user(user_id)
        if not user:
            raise SkillException(f"User with id {user_id} not found.", status_code=404)

        skill = get_skill_by_id(skill_id)
        if not skill:
            raise SkillException(f"Skill with id {skill_id} not found.", status_code=404)

        # Check if already assigned
        existing = db.session.execute(
            select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id)
        ).scalar_one_or_none()
        if existing:
            raise SkillException(f"Skill {skill_id} is already assigned to user {user_id}.", status_code=400)

        user_skill = UserSkill(user_id=user_id, skill_id=skill_id)
        db.session.add(user_skill)
        db.session.commit()
        return user_skill
    except Exception as e:
        db.session.rollback()
        if isinstance(e, SkillException):
            raise
        logger.error(f"Database error during skill assignment: {str(e)}")
        raise SkillException(f"Failed to assign skill: {str(e)}", status_code=500)

def remove_skill_from_user(user_id, skill_id):
    try:
        user_skill = db.session.execute(
            select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id)
        ).scalar_one_or_none()
        if not user_skill:
            raise SkillException(f"Skill {skill_id} is not assigned to user {user_id}.", status_code=404)

        db.session.delete(user_skill)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        if isinstance(e, SkillException):
            raise
        logger.error(f"Database error during skill removal: {str(e)}")
        raise SkillException(f"Failed to remove skill: {str(e)}", status_code=500)

def get_user_skills(user_id):
    try:
        user = get_user(user_id)
        if not user:
            raise SkillException(f"User with id {user_id} not found.", status_code=404)

        return db.session.execute(
            select(Skill).join(UserSkill).where(UserSkill.user_id == user_id)
        ).scalars().all()
    except Exception as e:
        if isinstance(e, SkillException):
            raise
        logger.error(f"Database error during getting user skills: {str(e)}")
        raise SkillException(f"Failed to get user skills: {str(e)}", status_code=500)

def get_skill_users(skill_id):
    try:
        skill = get_skill_by_id(skill_id)
        if not skill:
            raise SkillException(f"Skill with id {skill_id} not found.", status_code=404)

        return db.session.execute(
            select(User).join(UserSkill).where(UserSkill.skill_id == skill_id)
        ).scalars().all()
    except Exception as e:
        if isinstance(e, SkillException):
            raise
        logger.error(f"Database error during getting skill users: {str(e)}")
        raise SkillException(f"Failed to get skill users: {str(e)}", status_code=500)