from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    second_last_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    about_me = Column(String(700), nullable=True)
    profile_photo_url = Column(String(500), nullable=True)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    skills = relationship('Skill', secondary='user_skills', back_populates='users')
    resumes = relationship('Resume', back_populates='user')

    def __init__(self, name, last_name, second_last_name, email, password, about_me=None, profile_photo_url=None):
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name
        self.email = email
        self.password = password
        self.about_me = about_me
        self.profile_photo_url = profile_photo_url

    def __repr__(self):
        return f'<User {self.name} {self.last_name} {self.second_last_name}>'