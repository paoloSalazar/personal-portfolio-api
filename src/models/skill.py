from sqlalchemy import Column, Integer, String

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class Skill(db.Model):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name, description):
        self.name = name
        self.description = description  

    def __repr__(self):
        return f'<Skill {self.name}>'