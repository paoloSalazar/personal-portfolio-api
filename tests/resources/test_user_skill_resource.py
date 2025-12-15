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