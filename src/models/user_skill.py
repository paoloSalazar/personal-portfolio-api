from sqlalchemy import Column, Integer, ForeignKey

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class UserSkill(db.Model):
    __tablename__ = 'user_skills'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, skill_id):
        self.user_id = user_id
        self.skill_id = skill_id

    def __repr__(self):
        return f'<UserSkill user_id={self.user_id} skill_id={self.skill_id}>'