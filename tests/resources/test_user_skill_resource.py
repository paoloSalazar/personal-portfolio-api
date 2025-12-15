import pytest
import json
from src.services.user_service import create_user
from src.services.skill_service import create_skill

def test_get_user_skills(client, app):
    with app.app_context():
        # Create user and skills
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data1 = {'name': 'Skill 1', 'description': 'Desc 1'}
        skill_data2 = {'name': 'Skill 2', 'description': 'Desc 2'}
        skill1 = create_skill(skill_data1)
        skill2 = create_skill(skill_data2)

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Get user skills (should be empty)
        response = client.get(f'/users/{user.id}/skills', headers=headers)
        assert response.status_code == 200
        assert response.get_json() == []

        # Assign skills via service
        from src.services.user_skill_service import assign_skill_to_user
        assign_skill_to_user(user.id, skill1.id)
        assign_skill_to_user(user.id, skill2.id)

        # Get user skills
        response = client.get(f'/users/{user.id}/skills', headers=headers)
        assert response.status_code == 200
        skills = response.get_json()
        assert len(skills) == 2
        skill_names = [s['name'] for s in skills]
        assert 'Skill 1' in skill_names
        assert 'Skill 2' in skill_names

def test_assign_skill_to_user(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill', 'description': 'Test Description'}
        skill = create_skill(skill_data)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Assign skill
        response = client.post(f'/users/{user.id}/skills', json={'skill_id': skill.id}, headers=headers)
        assert response.status_code == 201
        assert response.get_json()['message'] == 'Skill assigned successfully'

def test_assign_skill_without_auth(client, app):
    response = client.post('/users/1/skills', json={'skill_id': 1})
    assert response.status_code == 401

def test_remove_skill_from_user(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill', 'description': 'Test Description'}
        skill = create_skill(skill_data)

        from src.services.user_skill_service import assign_skill_to_user
        assign_skill_to_user(user.id, skill.id)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Remove skill
        response = client.delete(f'/users/{user.id}/skills/{skill.id}', headers=headers)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Skill removed successfully'

def test_get_user_skills_nonexistent_user(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        response = client.get('/users/999/skills', headers=headers)
        assert response.status_code == 404

def test_get_user_skills_unauthorized(client, app):
    with app.app_context():
        # Create two users
        user_data1 = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user_data2 = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user_data1)
        user2 = create_user(user_data2)

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to access user2's skills
        response = client.get(f'/users/{user2.id}/skills', headers=headers)
        assert response.status_code == 403
        assert response.get_json()['error'] == 'Unauthorized to access this user\'s skills'

def test_assign_skill_unauthorized(client, app):
    with app.app_context():
        # Create two users and a skill
        user_data1 = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user_data2 = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user_data1)
        user2 = create_user(user_data2)
        skill_data = {'name': 'Test Skill', 'description': 'Test Description'}
        skill = create_skill(skill_data)

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to assign skill to user2
        response = client.post(f'/users/{user2.id}/skills', json={'skill_id': skill.id}, headers=headers)
        assert response.status_code == 403
        assert response.get_json()['error'] == 'Unauthorized to modify this user\'s skills'

def test_remove_skill_unauthorized(client, app):
    with app.app_context():
        # Create two users and a skill
        user_data1 = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user_data2 = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user_data1)
        user2 = create_user(user_data2)
        skill_data = {'name': 'Test Skill', 'description': 'Test Description'}
        skill = create_skill(skill_data)

        # Assign skill to user2
        from src.services.user_skill_service import assign_skill_to_user
        assign_skill_to_user(user2.id, skill.id)

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to remove skill from user2
        response = client.delete(f'/users/{user2.id}/skills/{skill.id}', headers=headers)
        assert response.status_code == 403
        assert response.get_json()['error'] == 'Unauthorized to modify this user\'s skills'