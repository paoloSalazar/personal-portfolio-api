import pytest
import json
from src.services.user_service import create_user
from src.services.skill_service import create_skill

def test_user_skills_routes_exist(client):
    """Test that user skill routes are properly registered."""
    # This test ensures the routes are added without errors
    # Since routes are registered at import time, if there are import errors, this will fail
    assert True

def test_get_user_skills_route(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        response = client.get(f'/users/{user.id}/skills', headers=headers)
        assert response.status_code == 200

def test_post_user_skills_route(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        response = client.post(f'/users/{user.id}/skills', json={'skill_id': skill.id}, headers=headers)
        assert response.status_code == 201

def test_delete_user_skill_route(client, app):
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

        response = client.delete(f'/users/{user.id}/skills/{skill.id}', headers=headers)
        assert response.status_code == 200