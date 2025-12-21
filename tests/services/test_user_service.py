import pytest
from src.services.user_service import create_user, get_user, get_all_users, update_user, delete_user, verify_password


# Unit tests for user_service functions
def test_create_user_service(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'second_last_name': 'Second', 'email': 'test@example.com', 'password': 'testpass', 'about_me': 'I am a test user'}
        user = create_user(user_data)
        assert user.name == 'Test User'
        assert user.last_name == 'Last'
        assert user.second_last_name == 'Second'
        assert user.email == 'test@example.com'
        assert user.about_me == 'I am a test user'
        assert user.id is not None

def test_get_user_service(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'second_last_name': 'Second', 'email': 'test@example.com', 'password': 'testpass'}
        user = create_user(user_data)
        retrieved = get_user(user.id)
        assert retrieved.id == user.id
        assert retrieved.name == 'Test User'
        assert retrieved.last_name == 'Last'

def test_get_all_users_service(app):
    with app.app_context():
        create_user({'name': 'User1', 'last_name': 'Last1', 'second_last_name': 'Second1', 'email': 'user1@example.com', 'password': 'pass1'})
        create_user({'name': 'User2', 'last_name': 'Last2', 'second_last_name': 'Second2', 'email': 'user2@example.com', 'password': 'pass2'})
        users = get_all_users()
        assert len(users) >= 2

def test_update_user_service(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'second_last_name': 'Second', 'email': 'test@example.com', 'password': 'testpass', 'about_me': 'Original about me'}
        user = create_user(user_data)
        update_data = {'about_me': 'Updated about me'}
        updated_user = update_user(user.id, update_data)
        assert updated_user.about_me == 'Updated about me'
