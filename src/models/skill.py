from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class Skill(db.Model):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    users = relationship('User', secondary='user_skills', back_populates='skills')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Skill {self.name}>'