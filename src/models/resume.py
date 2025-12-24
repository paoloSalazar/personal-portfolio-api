from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    summary = Column(String(1000), nullable=True)
    education = Column(String(2000), nullable=True)
    skills = Column(String(1000), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user = relationship('User', back_populates='resumes')
    skills = relationship('Skill', secondary='resume_skills', back_populates='resumes')

    def __init__(self, user_id, title, summary=None, education=None, start_date=None, end_date=None):
        self.user_id = user_id
        self.title = title
        self.summary = summary
        self.education = education
        self.start_date = start_date
        self.end_date = end_date
        
    def __repr__(self):
        return f'<Resume {self.title} for User ID {self.user_id}>'