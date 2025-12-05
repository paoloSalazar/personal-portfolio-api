import pytest
from src.models.skill import Skill
from src.schemas.skill_schema import SkillSchema

def test_create_skill(client):
    response = client.post('/api/skills', json={
        'name': 'New Skill',
        'description': 'Skill Description'
    })
    assert response.status_code == 201, f"POST failed: {response.data}"
    assert 'id' in response.json
    assert response.json['name'] == 'New Skill'
    assert response.json['description'] == 'Skill Description'

def test_get_all_skills(client):
    """Test creating and retrieving skills"""
    # Create skills via API
    post1 = client.post('/api/skills', json={
        'name': 'Skill 1',
        'description': 'Description 1'
    })
    assert post1.status_code == 201, f"POST failed: {post1.data}"

    post2 = client.post('/api/skills', json={
        'name': 'Skill 2',
        'description': 'Description 2'
    })
    assert post2.status_code == 201, f"POST failed: {post2.data}"

    # Get all skills
    response = client.get('/api/skills')
    assert response.status_code == 200, f"GET failed: {response.data}"
    assert len(response.json) == 2