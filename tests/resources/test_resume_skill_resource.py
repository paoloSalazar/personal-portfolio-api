import pytest
from src.services.user_service import create_user
from src.services.skill_service import create_skill
from src.services.resume_service import create_resume

def test_get_resume_skills(client, app):
    with app.app_context():
        # Create user, skill, resume
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Python'}
        skill = create_skill(skill_data)
        resume = create_resume(user.id, 'Test Resume')

        # Login to get token
        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Get resume skills (should be empty)
        response = client.get(f'/users/{user.id}/resumes/{resume.id}/skills', headers=headers)
        assert response.status_code == 200
        assert response.get_json() == []

        # Assign skill
        from src.services.resume_skill_service import assign_skill_to_resume
        assign_skill_to_resume(resume.id, skill.id)

        # Get resume skills
        response = client.get(f'/users/{user.id}/resumes/{resume.id}/skills', headers=headers)
        assert response.status_code == 200
        skills = response.get_json()
        assert len(skills) == 1
        assert skills[0]['name'] == 'Python'

def test_assign_skill_to_resume(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'JavaScript'}
        skill = create_skill(skill_data)
        resume = create_resume(user.id, 'Test Resume')

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Assign skill
        response = client.post(f'/users/{user.id}/resumes/{resume.id}/skills', json={'skill_id': skill.id}, headers=headers)
        assert response.status_code == 201
        assert response.get_json()['message'] == 'Skill assigned successfully'

def test_remove_skill_from_resume(client, app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'SQL'}
        skill = create_skill(skill_data)
        resume = create_resume(user.id, 'Test Resume')

        from src.services.resume_skill_service import assign_skill_to_resume
        assign_skill_to_resume(resume.id, skill.id)

        login_response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Remove skill
        response = client.delete(f'/users/{user.id}/resumes/{resume.id}/skills/{skill.id}', headers=headers)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Skill removed successfully'

def test_unauthorized_resume_skill_access(client, app):
    with app.app_context():
        # Create two users
        user_data1 = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user_data2 = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user_data1)
        user2 = create_user(user_data2)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)
        resume = create_resume(user2.id, 'Test Resume')

        # Login as user1
        login_response = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'password'})
        token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {token}'}

        # Try to access user2's resume skills
        response = client.get(f'/users/{user2.id}/resumes/{resume.id}/skills', headers=headers)
        assert response.status_code == 403