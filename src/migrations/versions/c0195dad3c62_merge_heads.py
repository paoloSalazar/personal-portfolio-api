"""Merge heads

Revision ID: c0195dad3c62
Revises: 466f168ada4d, added_user_skill_entity
Create Date: 2025-12-15 09:07:45.076903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0195dad3c62'
down_revision = ('466f168ada4d', 'added_user_skill_entity')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
