from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

try:
    from utils.extensions import db
except ImportError:
    from src.utils.extensions import db

class UserContact(db.Model):
    __tablename__ = 'user_contacts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contacttype_id = Column(Integer, ForeignKey('contact_types.id'), nullable=False)
    link_or_number = Column(String(255), nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    user = relationship('User', backref='contacts')
    contact_type = relationship('ContactType', backref='user_contacts')

    def __init__(self, user_id, contacttype_id, link_or_number):
        self.user_id = user_id
        self.contacttype_id = contacttype_id
        self.link_or_number = link_or_number

    def __repr__(self):
        return f'<UserContact user_id={self.user_id} contacttype_id={self.contacttype_id} value={self.link_or_number}>'