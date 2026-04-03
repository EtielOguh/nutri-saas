"""Add email, phone, gender, initial_weight, notes to Cliente.

Revision ID: 001
Revises: 
Create Date: 2026-04-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add new columns to clientes table."""
    op.add_column('clientes', sa.Column('email', sa.String(255), nullable=True))
    op.add_column('clientes', sa.Column('phone', sa.String(20), nullable=True))
    op.add_column('clientes', sa.Column('gender', sa.String(20), nullable=True))
    op.add_column('clientes', sa.Column('initial_weight', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('notes', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove new columns from clientes table."""
    op.drop_column('clientes', 'notes')
    op.drop_column('clientes', 'initial_weight')
    op.drop_column('clientes', 'gender')
    op.drop_column('clientes', 'phone')
    op.drop_column('clientes', 'email')
