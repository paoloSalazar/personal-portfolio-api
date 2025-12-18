import pytest
from src.services.user_skill_service import assign_skill_to_user, remove_skill_from_user, get_user_skills, get_skill_users
from src.services.user_service import create_user
from src.services.skill_service import create_skill
from src.exceptions.skill_exceptions import SkillException

def test_assign_skill_to_user(app):
    with app.app_context():
        # Create user and skill
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)

        # Assign skill
        user_skill = assign_skill_to_user(user.id, skill.id)
        assert user_skill.user_id == user.id
        assert user_skill.skill_id == skill.id

def test_assign_skill_to_nonexistent_user(app):
    with app.app_context():
        with pytest.raises(SkillException) as exc_info:
            assign_skill_to_user(999, 1)
        assert exc_info.value.status_code == 404

def test_assign_skill_to_nonexistent_skill(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        with pytest.raises(SkillException) as exc_info:
            assign_skill_to_user(user.id, 999)
        assert exc_info.value.status_code == 404

def test_assign_duplicate_skill(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)

        assign_skill_to_user(user.id, skill.id)
        with pytest.raises(SkillException) as exc_info:
            assign_skill_to_user(user.id, skill.id)
        assert exc_info.value.status_code == 400

def test_remove_skill_from_user(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)

        assign_skill_to_user(user.id, skill.id)
        result = remove_skill_from_user(user.id, skill.id)
        assert result is True

def test_remove_nonexistent_skill_assignment(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)

        with pytest.raises(SkillException) as exc_info:
            remove_skill_from_user(user.id, skill.id)
        assert exc_info.value.status_code == 404

def test_get_user_skills(app):
    with app.app_context():
        user_data = {'name': 'Test User', 'last_name': 'Last', 'email': 'test@example.com', 'password': 'password'}
        user = create_user(user_data)
        skill_data1 = {'name': 'Skill 1'}
        skill_data2 = {'name': 'Skill 2'}
        skill1 = create_skill(skill_data1)
        skill2 = create_skill(skill_data2)

        assign_skill_to_user(user.id, skill1.id)
        assign_skill_to_user(user.id, skill2.id)

        skills = get_user_skills(user.id)
        assert len(skills) == 2
        skill_names = [s.name for s in skills]
        assert 'Skill 1' in skill_names
        assert 'Skill 2' in skill_names

def test_get_user_skills_nonexistent_user(app):
    with app.app_context():
        with pytest.raises(SkillException) as exc_info:
            get_user_skills(999)
        assert exc_info.value.status_code == 404

def test_get_skill_users(app):
    with app.app_context():
        user_data1 = {'name': 'User 1', 'last_name': 'Last', 'email': 'user1@example.com', 'password': 'password'}
        user_data2 = {'name': 'User 2', 'last_name': 'Last', 'email': 'user2@example.com', 'password': 'password'}
        user1 = create_user(user_data1)
        user2 = create_user(user_data2)
        skill_data = {'name': 'Test Skill'}
        skill = create_skill(skill_data)

        assign_skill_to_user(user1.id, skill.id)
        assign_skill_to_user(user2.id, skill.id)

        users = get_skill_users(skill.id)
        assert len(users) == 2
        user_names = [u.name for u in users]
        assert 'User 1' in user_names
        assert 'User 2' in user_names

def test_get_skill_users_nonexistent_skill(app):
    with app.app_context():
        with pytest.raises(SkillException) as exc_info:
            get_skill_users(999)
        assert exc_info.value.status_code == 404