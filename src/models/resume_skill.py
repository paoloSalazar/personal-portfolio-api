from sqlalchemy import Column, Integer, ForeignKey

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class ResumeSkill(db.Model):
    __tablename__ = 'resume_skills'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, resume_id, skill_id):
        self.resume_id = resume_id
        self.skill_id = skill_id

    def __repr__(self):
        return f'<ResumeSkill resume_id={self.resume_id} skill_id={self.skill_id}>'