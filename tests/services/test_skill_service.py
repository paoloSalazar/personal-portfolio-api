import pytest
from src.services.skill_service import create_skill, get_all_skills, get_skill_by_id

# Unit tests for user_service functions
def test_create_skill_service(app):
    with app.app_context():
        skill_data = {'name': 'Test Skill', 'description': 'Test Description'}
        skill = create_skill(skill_data)
        assert skill.name == 'Test Skill'
        assert skill.description == 'Test Description'  
        assert skill.id is not None

def test_get_all_skills_service(app):
    with app.app_context():
        skill_data1 = {'name': 'Skill One', 'description': 'Description One'}
        skill_data2 = {'name': 'Skill Two', 'description': 'Description Two'}
        create_skill(skill_data1)
        create_skill(skill_data2)

        skills = get_all_skills()
        assert len(skills) >= 2  # At least the two we just added

def test_get_skill_by_id_service(app):
    with app.app_context():
        skill_data = {'name': 'Unique Skill', 'description': 'Unique Description'}
        skill = create_skill(skill_data)

        fetched_skill = get_skill_by_id(skill.id)
        assert fetched_skill is not None
        assert fetched_skill.name == 'Unique Skill'
        assert fetched_skill.description == 'Unique Description'