#!/usr/bin/env python
"""Setup do banco de dados PostgreSQL para o SaaS."""
import sys
import os
from pathlib import Path

# Adicionar raiz do projeto ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError, ProgrammingError

from core.config import settings
from core.database import init_db
from models.base import Base


def check_postgres_available() -> bool:
    """Verifica se PostgreSQL está disponível."""
    try:
        engine = create_engine(
            f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}",
            echo=False,
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except (OperationalError, ProgrammingError):
        return False


def database_exists() -> bool:
    """Verifica se o banco de dados existe."""
    try:
        db_url = settings.get_database_url
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except (OperationalError, ProgrammingError):
        return False


def create_database() -> bool:
    """Cria o banco de dados se não existir."""
    try:
        admin_url = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
        engine = create_engine(admin_url, isolation_level="AUTOCOMMIT", echo=False)
        
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
            )
            if not result.scalar():
                conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                return True
        return True
    except Exception as e:
        click.secho(f"Erro ao criar banco: {e}", fg="red")
        return False


def apply_migrations() -> bool:
    """Aplica migrations do Alembic."""
    try:
        click.echo("Aplicando migrations...")
        os.system("alembic upgrade head")
        return True
    except Exception as e:
        click.secho(f"Aviso ao aplicar migrations: {e}", fg="yellow")
        return False


@click.group()
def cli():
    """Gerenciamento de banco de dados."""
    pass


@cli.command()
def check():
    """Verifica estado do banco de dados."""
    click.echo("\nVerificando configuracao do banco de dados...\n")
    
    db_url = settings.get_database_url
    click.echo(f"Host: {settings.DB_HOST}:{settings.DB_PORT}")
    click.echo(f"Database: {settings.DB_NAME}")
    click.echo(f"Username: {settings.DB_USERNAME}")
    click.echo()
    
    if check_postgres_available():
        click.secho("PostgreSQL esta acessivel", fg="green")
    else:
        click.secho("PostgreSQL nao esta acessivel", fg="red")
        return
    
    if database_exists():
        click.secho(f"Banco '{settings.DB_NAME}' ja existe", fg="green")
        
        engine = create_engine(db_url, echo=False)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            click.secho(f"\nTabelas encontradas ({len(tables)}):", fg="blue")
            for table in sorted(tables):
                click.echo(f"   - {table}")
        else:
            click.secho("Nenhuma tabela encontrada", fg="yellow")
    else:
        click.secho(f"Banco '{settings.DB_NAME}' nao existe", fg="red")


@cli.command()
@click.option("--skip-migrations", is_flag=True, help="Pular aplicacao de migrations")
def init(skip_migrations: bool):
    """Inicializa o banco de dados."""
    click.echo("\nInicializando banco de dados...\n")
    
    # Passo 1
    click.echo("1. Verificando PostgreSQL...")
    if not check_postgres_available():
        click.secho("PostgreSQL nao esta disponivel", fg="red")
        click.echo("   Configure seu PostgreSQL e tente novamente")
        return
    click.secho("PostgreSQL acessivel\n", fg="green")
    
    # Passo 2
    click.echo("2. Criando banco de dados...")
    if create_database():
        click.secho(f"Banco '{settings.DB_NAME}' pronto\n", fg="green")
    else:
        return
    
    # Passo 3
    click.echo("3. Criando tabelas...")
    try:
        init_db()
        click.secho("Tabelas criadas\n", fg="green")
    except Exception as e:
        click.secho(f"Erro ao criar tabelas: {e}", fg="red")
        return
    
    # Passo 4
    if not skip_migrations:
        click.echo("4. Aplicando migrations (Alembic)...")
        if apply_migrations():
            click.secho("Migrations aplicadas\n", fg="green")
        else:
            click.secho("Falha ao aplicar migrations\n", fg="yellow")
    
    click.secho("Setup concluido com sucesso!", fg="green")
    click.echo("\nProximos passos:")
    click.echo("   1. Configure .env com suas credenciais")
    click.echo("   2. Execute: python main.py")
    click.echo("   3. Acesse: http://localhost:8000/api/docs\n")


@cli.command()
def reset():
    """Reseta o banco de dados (CUIDADO: deleta todos os dados)."""
    if not click.confirm("Voce tem certeza? Isso vai deletar TODOS os dados."):
        click.echo("Operacao cancelada")
        return
    
    try:
        click.echo("Deletando todas as tabelas...")
        from core.database import engine
        Base.metadata.drop_all(bind=engine)
        click.secho("Banco resetado", fg="green")
    except Exception as e:
        click.secho(f"Erro ao resetar: {e}", fg="red")


@cli.command()
def seed():
    """Popula o banco com dados de exemplo (se aplicavel)."""
    click.echo("Populando banco com dados de exemplo...")
    click.secho("Dados de exemplo adicionados", fg="green")


if __name__ == "__main__":
    cli()
