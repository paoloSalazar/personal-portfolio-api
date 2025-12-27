from flask_restful import Resource
from flask import request
import logging

try:
    from schemas.resume_schema import ResumeSchema
    from services.resume_service import create_resume, get_resume, get_user_resumes, update_resume, delete_resume
    from utils.auth import jwt_required, get_current_user_id
except ImportError:
    from src.schemas.resume_schema import ResumeSchema
    from src.services.resume_service import create_resume, get_resume, get_user_resumes, update_resume, delete_resume
    from src.utils.auth import jwt_required, get_current_user_id

resumes_schema = ResumeSchema(many=True)
resume_schema = ResumeSchema()

logger = logging.getLogger(__name__)

class ResumeResource(Resource):

    # @jwt_required
    def get(self, user_id, resume_id=None):
        # current_user_id = str(get_current_user_id())
        # if str(user_id) != current_user_id:
        #     logger.warning(f"User {current_user_id} attempted to access resume for user {user_id}")
        #     return {'error': 'Unauthorized to access this user\'s resumes'}, 403

        try:
            if resume_id:
                resume = get_resume(resume_id)
                if not resume or resume.user_id != user_id:
                    return {'error': 'Resume not found'}, 404
                logger.info(f"Returning resume {resume_id} for user {user_id}")
                return resume_schema.dump(resume), 200
            else:
                resumes = get_user_resumes(user_id)
                logger.info(f"Returning {len(resumes)} resumes for user {user_id}")
                return resumes_schema.dump(resumes), 200
        except ValueError as e:
            logger.error(f"Failed to get resumes: {e}")
            return {'error': str(e)}, 400

    @jwt_required
    def post(self, user_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to create resume for user {user_id}")
            return {'error': 'Unauthorized to create resume for this user'}, 403

        try:
            data = request.get_json()
            title = data.get('title')
            if not title:
                return {'error': 'title is required'}, 400
            resume = create_resume(
                user_id=user_id,
                title=title,
                summary=data.get('summary'),
                education=data.get('education'),
                start_date=data.get('start_date'),
                end_date=data.get('end_date')
            )
            logger.info(f"Resume created for user {user_id}")
            return resume_schema.dump(resume), 201
        except ValueError as e:
            logger.error(f"Resume creation failed: {e}")
            return {'error': str(e)}, 400

    @jwt_required
    def put(self, user_id, resume_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to update resume for user {user_id}")
            return {'error': 'Unauthorized to update this user\'s resumes'}, 403

        try:
            resume = get_resume(resume_id)
            if not resume or resume.user_id != user_id:
                return {'error': 'Resume not found'}, 404

            data = request.get_json()
            updated_resume = update_resume(resume_id, **data)
            logger.info(f"Resume {resume_id} updated for user {user_id}")
            return resume_schema.dump(updated_resume), 200
        except ValueError as e:
            logger.error(f"Resume update failed: {e}")
            return {'error': str(e)}, 400

    @jwt_required
    def delete(self, user_id, resume_id):
        current_user_id = str(get_current_user_id())
        if str(user_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to delete resume for user {user_id}")
            return {'error': 'Unauthorized to delete this user\'s resumes'}, 403

        try:
            resume = get_resume(resume_id)
            if not resume or resume.user_id != user_id:
                return {'error': 'Resume not found'}, 404

            delete_resume(resume_id)
            logger.info(f"Resume {resume_id} deleted for user {user_id}")
            return {'message': 'Resume deleted successfully'}, 200
        except ValueError as e:
            logger.error(f"Resume deletion failed: {e}")
            return {'error': str(e)}, 400