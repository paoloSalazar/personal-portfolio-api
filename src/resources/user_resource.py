from flask_restful import Resource, Api
from flask import request

try:
    from models.user import User
    from schemas.user_schema import UserSchema
    from services.user_service import create_user, get_user, get_all_users, update_user, delete_user
except ImportError:
    from src.models.user import User
    from src.schemas.user_schema import UserSchema
    from src.services.user_service import create_user, get_user, get_all_users, update_user, delete_user

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = get_user(user_id)
            if user:
                return user_schema.dump(user), 200
            return {'message': 'User not found'}, 404
        else:
            users = get_all_users()
            return users_schema.dump(users), 200

    def post(self):
        user_data = request.get_json()
        user = create_user(user_data)
        return user_schema.dump(user), 201

    def put(self, user_id):
        user_data = request.get_json()
        user = update_user(user_id, user_data)
        if user:
            return user_schema.dump(user), 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        if delete_user(user_id):
            return '', 204
        return {'message': 'User not found'}, 404