import pytest
from src.models.resume_skill import ResumeSkill


def test_resume_skill_init():
    """Test ResumeSkill initialization."""
    resume_skill = ResumeSkill(resume_id=1, skill_id=2)
    assert resume_skill.resume_id == 1
    assert resume_skill.skill_id == 2


def test_resume_skill_repr():
    """Test ResumeSkill __repr__ method."""
    resume_skill = ResumeSkill(resume_id=1, skill_id=2)
    assert repr(resume_skill) == '<ResumeSkill resume_id=1 skill_id=2>'


def test_resume_skill_attributes():
    """Test ResumeSkill has required attributes."""
    resume_skill = ResumeSkill(resume_id=10, skill_id=20)
    assert hasattr(resume_skill, 'id')
    assert hasattr(resume_skill, 'resume_id')
    assert hasattr(resume_skill, 'skill_id')
    assert hasattr(resume_skill, 'created_at')
    assert hasattr(resume_skill, 'updated_at')