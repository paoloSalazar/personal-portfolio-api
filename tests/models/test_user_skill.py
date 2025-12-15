import pytest
from src.models.user_skill import UserSkill


def test_user_skill_init():
    """Test UserSkill initialization."""
    user_skill = UserSkill(user_id=1, skill_id=2)
    assert user_skill.user_id == 1
    assert user_skill.skill_id == 2


def test_user_skill_repr():
    """Test UserSkill __repr__ method."""
    user_skill = UserSkill(user_id=1, skill_id=2)
    assert repr(user_skill) == '<UserSkill user_id=1 skill_id=2>'


def test_user_skill_attributes():
    """Test UserSkill has required attributes."""
    user_skill = UserSkill(user_id=10, skill_id=20)
    assert hasattr(user_skill, 'id')
    assert hasattr(user_skill, 'user_id')
    assert hasattr(user_skill, 'skill_id')
    assert hasattr(user_skill, 'created_at')
    assert hasattr(user_skill, 'updated_at')