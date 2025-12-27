try:
    from models.resume import Resume
    from models.user import User
    from services.user_service import get_user
    from utils.extensions import db
except ImportError:
    from src.models.resume import Resume
    from src.models.user import User
    from src.services.user_service import get_user
    from src.utils.extensions import db

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

def create_resume(user_id, title, summary=None, education=None, start_date=None, end_date=None):
    try:
        user = get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        resume = Resume(user_id=user_id, title=title, summary=summary, education=education, start_date=start_date, end_date=end_date)
        db.session.add(resume)
        db.session.commit()
        return resume
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error during resume creation: {str(e)}")
        raise ValueError(f"Failed to create resume: {str(e)}")

def get_resume(resume_id):
    try:
        return db.session.execute(
            select(Resume).where(Resume.id == resume_id)
        ).scalar_one_or_none()
    except Exception as e:
        logger.error(f"Database error during getting resume: {str(e)}")
        raise ValueError(f"Failed to get resume: {str(e)}")

def get_user_resumes(user_id):
    try:
        user = get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        return db.session.execute(
            select(Resume).where(Resume.user_id == user_id)
        ).scalars().all()
    except Exception as e:
        logger.error(f"Database error during getting user resumes: {str(e)}")
        raise ValueError(f"Failed to get user resumes: {str(e)}")

def update_resume(resume_id, **kwargs):
    try:
        resume = get_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found.")

        for key, value in kwargs.items():
            if hasattr(resume, key):
                setattr(resume, key, value)

        db.session.commit()
        return resume
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error during resume update: {str(e)}")
        raise ValueError(f"Failed to update resume: {str(e)}")

def delete_resume(resume_id):
    try:
        resume = get_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found.")

        db.session.delete(resume)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error during resume deletion: {str(e)}")
        raise ValueError(f"Failed to delete resume: {str(e)}")