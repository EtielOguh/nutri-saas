"""Fix ConfiguracaoNutricionista - add id as PK.

Revision ID: 002
Revises: 001
Create Date: 2026-04-03 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add id column as primary key to configuracoes_nutricionista table."""
    # Note: SQLite doesn't support modifying PRIMARY KEY directly
    # We'll create a new table and migrate data
    
    # Create new table with correct schema
    op.execute("""
        CREATE TABLE configuracoes_nutricionista_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutricionista_id INTEGER NOT NULL UNIQUE,
            logo_url VARCHAR(512),
            cor_primaria VARCHAR(7) DEFAULT '#0066CC' NOT NULL,
            valor_consulta FLOAT NOT NULL DEFAULT 0.0,
            link_agendamento VARCHAR(512),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (nutricionista_id) REFERENCES nutricionistas (id) ON DELETE CASCADE
        )
    """)
    
    # Copy data from old table
    op.execute("""
        INSERT INTO configuracoes_nutricionista_new 
            (nutricionista_id, logo_url, cor_primaria, valor_consulta, link_agendamento, created_at, updated_at)
        SELECT nutricionista_id, logo_url, cor_primaria, valor_consulta, link_agendamento, created_at, updated_at
        FROM configuracoes_nutricionista
    """)
    
    # Drop old table
    op.execute("DROP TABLE configuracoes_nutricionista")
    
    # Rename new table
    op.execute("ALTER TABLE configuracoes_nutricionista_new RENAME TO configuracoes_nutricionista")
    
    # Recreate indices
    op.create_index("idx_config_nutricionista_id", "configuracoes_nutricionista", ["nutricionista_id"])


def downgrade() -> None:
    """Revert to original schema without id column."""
    op.execute("""
        CREATE TABLE configuracoes_nutricionista_new (
            nutricionista_id INTEGER PRIMARY KEY NOT NULL,
            logo_url VARCHAR(512),
            cor_primaria VARCHAR(7) DEFAULT '#0066CC' NOT NULL,
            valor_consulta FLOAT NOT NULL DEFAULT 0.0,
            link_agendamento VARCHAR(512),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (nutricionista_id) REFERENCES nutricionistas (id) ON DELETE CASCADE
        )
    """)
    
    op.execute("""
        INSERT INTO configuracoes_nutricionista_new
            (nutricionista_id, logo_url, cor_primaria, valor_consulta, link_agendamento, created_at, updated_at)
        SELECT nutricionista_id, logo_url, cor_primaria, valor_consulta, link_agendamento, created_at, updated_at
        FROM configuracoes_nutricionista
    """)
    
    op.execute("DROP TABLE configuracoes_nutricionista")
    op.execute("ALTER TABLE configuracoes_nutricionista_new RENAME TO configuracoes_nutricionista")
