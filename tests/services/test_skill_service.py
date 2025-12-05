import pytest
from src.services.skill_service import create_skill

# Unit tests for user_service functions
def test_create_skill_service(app):
    with app.app_context():
        skill_data = {'name': 'Test Skill', 'description': 'Test Description'}
        skill = create_skill(skill_data)
        assert skill.name == 'Test Skill'
        assert skill.description == 'Test Description'  
        assert skill.id is not None