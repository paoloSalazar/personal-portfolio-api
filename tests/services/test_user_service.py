import pytest
from src.services.user_service import create_user, get_user, get_all_users, update_user, delete_user, verify_password


# Unit tests for user_service functions
def test_get_all_users_service(app):
    with app.app_context():
        create_user({'name': 'User1', 'email': 'user1@example.com', 'password': 'pass1'})
        create_user({'name': 'User2', 'email': 'user2@example.com', 'password': 'pass2'})
        users = get_all_users()
        assert len(users) >= 2
        
def test_create_user_service(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpass'}
        user = create_user(user_data)
        assert user.name == 'Test User'
        assert user.email == 'test@example.com'
        assert user.id is not None


