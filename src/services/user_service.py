try:
    from models.user import User
    from schemas.user_schema import UserSchema
    from utils.extensions import db, bcrypt
    from exceptions.user_exceptions import UserAlreadyExistsException, UserDatabaseException
except ImportError:
    from src.models.user import User
    from src.schemas.user_schema import UserSchema
    from src.utils.extensions import db, bcrypt
    from src.exceptions.user_exceptions import UserAlreadyExistsException, UserDatabaseException

from sqlalchemy import select
import logging
logger = logging.getLogger(__name__)
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)

def create_user(data):
    try:
        # Hash the password before saving
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Create user instance directly instead of using schema.load
        new_user = User(
            name=data['name'],
            last_name=data['last_name'],
            second_last_name=data.get('second_last_name'),
            email=data['email'],
            password=password_hash
        )

        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        if "Duplicate entry" in str(e) and "email" in str(e):
            logger.error(f"Attempted to create user with duplicate email: {data['email']}")
            raise UserAlreadyExistsException(data['email'])
        else:
            logger.error(f"Database error during user creation: {str(e)}")
            raise UserDatabaseException(f"Failed to create user: {str(e)}")

def get_user(user_id):
    return db.session.get(User, user_id)

def get_all_users():
    return db.session.execute(select(User)).scalars().all()

def update_user(user_id, data):
    user = db.session.get(User, user_id)
    if user:
        # Update fields directly
        if 'name' in data:
            user.name = data['name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'second_last_name' in data:
            user.second_last_name = data['second_last_name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        db.session.commit()
        return user
    return None

def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def verify_password(email, password):
    user = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None