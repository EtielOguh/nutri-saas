"""Add CRN field to Nutricionista.

Revision ID: 003
Revises: 002
Create Date: 2026-04-03 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add CRN column to nutricionistas table."""
    op.add_column('nutricionistas', sa.Column('crn', sa.String(50), nullable=True))
    op.create_index('idx_nutricionista_crn', 'nutricionistas', ['crn'])


def downgrade() -> None:
    """Remove CRN column from nutricionistas table."""
    op.drop_index('idx_nutricionista_crn', 'nutricionistas')
    op.drop_column('nutricionistas', 'crn')
