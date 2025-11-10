from models.user import User
from schemas.user_schema import UserSchema
from utils.extensions import db, bcrypt

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def create_user(data):
    # Hash the password before saving
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = password_hash

    new_user = user_schema.load(data)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def update_user(user_id, data):
    user = User.query.get(user_id)
    if user:
        # Hash password if it's being updated
        if 'password' in data:
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user_schema.load(data, instance=user, partial=True)
        db.session.commit()
        return user
    return None

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None