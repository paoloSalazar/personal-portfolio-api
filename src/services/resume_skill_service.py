try:
    from models.resume import Resume
    from models.skill import Skill
    from models.resume_skill import ResumeSkill
    from services.resume_service import get_resume
    from services.skill_service import get_skill_by_id
    from utils.extensions import db
except ImportError:
    from src.models.resume import Resume
    from src.models.skill import Skill
    from src.models.resume_skill import ResumeSkill
    from src.services.resume_service import get_resume
    from src.services.skill_service import get_skill_by_id
    from src.utils.extensions import db

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

def assign_skills_to_resume(resume_id, skill_ids):
    try:
        resume = get_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found.")

        if not isinstance(skill_ids, list) or not skill_ids:
            raise ValueError("skill_ids must be a non-empty list.")

        assigned = []
        errors = []

        for skill_id in skill_ids:
            try:
                skill = get_skill_by_id(skill_id)
                if not skill:
                    errors.append(f"Skill with id {skill_id} not found.")
                    continue

                # Check if already assigned
                existing = db.session.execute(
                    select(ResumeSkill).where(ResumeSkill.resume_id == resume_id, ResumeSkill.skill_id == skill_id)
                ).scalar_one_or_none()
                if existing:
                    errors.append(f"Skill {skill_id} is already assigned to resume {resume_id}.")
                    continue

                resume_skill = ResumeSkill(resume_id=resume_id, skill_id=skill_id)
                db.session.add(resume_skill)
                assigned.append(skill_id)
            except Exception as e:
                errors.append(f"Error assigning skill {skill_id}: {str(e)}")

        db.session.commit()
        return {"assigned": assigned, "errors": errors}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error during skills assignment to resume: {str(e)}")
        raise ValueError(f"Failed to assign skills to resume: {str(e)}")

def remove_skill_from_resume(resume_id, skill_id):
    try:
        resume_skill = db.session.execute(
            select(ResumeSkill).where(ResumeSkill.resume_id == resume_id, ResumeSkill.skill_id == skill_id)
        ).scalar_one_or_none()
        if not resume_skill:
            raise ValueError(f"Skill {skill_id} is not assigned to resume {resume_id}.")

        db.session.delete(resume_skill)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error during skill removal from resume: {str(e)}")
        raise ValueError(f"Failed to remove skill from resume: {str(e)}")

def get_resume_skills(resume_id):
    try:
        resume = get_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found.")

        return db.session.execute(
            select(Skill).join(ResumeSkill).where(ResumeSkill.resume_id == resume_id)
        ).scalars().all()
    except Exception as e:
        logger.error(f"Database error during getting resume skills: {str(e)}")
        raise ValueError(f"Failed to get resume skills: {str(e)}")

def get_skill_resumes(skill_id):
    try:
        skill = get_skill_by_id(skill_id)
        if not skill:
            raise ValueError(f"Skill with id {skill_id} not found.")

        return db.session.execute(
            select(Resume).join(ResumeSkill).where(ResumeSkill.skill_id == skill_id)
        ).scalars().all()
    except Exception as e:
        logger.error(f"Database error during getting skill resumes: {str(e)}")
        raise ValueError(f"Failed to get skill resumes: {str(e)}")