"""Remove cor_primaria from ConfiguracaoNutricionista.

Revision ID: 004
Revises: 003
Create Date: 2026-04-03 23:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove cor_primaria column from configuracoes_nutricionista table."""
    op.drop_column('configuracoes_nutricionista', 'cor_primaria')


def downgrade() -> None:
    """Re-add cor_primaria column to configuracoes_nutricionista table."""
    op.add_column(
        'configuracoes_nutricionista',
        sa.Column('cor_primaria', sa.String(7), nullable=False, server_default='#0066CC')
    )
