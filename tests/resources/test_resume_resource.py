import pytest
import json
from src.services.user_service import create_user

def test_get_user_resumes(client, app):
    with app.app_context():
        # Create user
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Get user resumes (should be empty)
        response = client.get(f'/users/{user.id}/resumes', headers=headers)
        assert response.status_code == 200
        assert response.get_json() == []

def test_create_resume(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Create resume
        resume_data = {'title': 'Software Engineer', 'summary': 'Experienced developer'}
        response = client.post(f'/users/{user.id}/resumes', json=resume_data, headers=headers)
        assert response.status_code == 201
        resume = response.get_json()
        assert resume['title'] == 'Software Engineer'
        assert resume['summary'] == 'Experienced developer'
        assert resume['user_id'] == user.id

def test_get_resume(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        from src.services.resume_service import create_resume
        resume = create_resume(user.id, 'Test Resume')

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Get specific resume
        response = client.get(f'/users/{user.id}/resumes/{resume.id}', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == resume.id
        assert data['title'] == 'Test Resume'

def test_update_resume(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        from src.services.resume_service import create_resume
        resume = create_resume(user.id, 'Test Resume')

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Update resume
        update_data = {'title': 'Updated Resume', 'summary': 'Updated summary'}
        response = client.put(f'/users/{user.id}/resumes/{resume.id}', json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Resume'
        assert data['summary'] == 'Updated summary'

def test_delete_resume(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)

        from src.services.resume_service import create_resume
        resume = create_resume(user.id, 'Test Resume')

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Delete resume
        response = client.delete(f'/users/{user.id}/resumes/{resume.id}', headers=headers)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Resume deleted successfully'

def test_unauthorized_access(client, app):
    with app.app_context():
        # Create two users
        user_data1 = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user_data2 = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user_data1)
        user2 = create_user(user_data2)

        from src.services.resume_service import create_resume
        resume = create_resume(user2.id, 'Test Resume')

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to access user2's resume
        response = client.get(f'/users/{user2.id}/resumes/{resume.id}', headers=headers)
        assert response.status_code == 403