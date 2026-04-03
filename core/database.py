"""Configuração de banco de dados com SQLAlchemy e PostgreSQL."""
from typing import Generator
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, QueuePool

from core.config import settings


def create_database_engine() -> Engine:
    """
    Cria a engine do SQLAlchemy com configurações otimizadas para SaaS.
    
    Returns:
        Engine: Engine do SQLAlchemy configurada
    """
    database_url = settings.get_database_url
    
    # Configurações para PostgreSQL em produção
    engine_kwargs = {
        "pool_pre_ping": True,  # Valida conexão antes de usar (evita stale connections)
        "echo": settings.DB_ECHO,  # Log SQL em desenvolvimento
        "future": True,  # Usar SQLAlchemy 2.0 style
    }
    
    if database_url.startswith("sqlite"):
        # SQLite (apenas desenvolvimento)
        engine_kwargs.update({
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        })
    else:
        # PostgreSQL (produção)
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
            "pool_recycle": settings.DB_POOL_RECYCLE,
            "pool_pre_ping": True,
        })
    
    engine = create_engine(database_url, **engine_kwargs)
    
    # Event listener para logging de eventos de pool (debug)
    if settings.DEBUG:
        @event.listens_for(Engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            print(f"[DB] Nova conexão criada: {id(dbapi_conn)}")
        
        @event.listens_for(Engine, "close")
        def receive_close(dbapi_conn, connection_record):
            print(f"[DB] Conexão fechada: {id(dbapi_conn)}")
    
    return engine


# Criar engine e SessionLocal
engine = create_database_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para injetar a sessão do banco em rotas FastAPI.
    
    Yields:
        Session: Sessão ativa do banco de dados
        
    Example:
        @app.get("/users/")
        def list_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa o banco de dados criando todas as tabelas.
    Útil para primeiro setup ou testes.
    """
    from models.base import Base
    Base.metadata.create_all(bind=engine)


def close_db() -> None:
    """
    Fecha todas as conexões do pool.
    Útil ao desligar a aplicação.
    """
    engine.dispose()


# Event listeners para PostgreSQL
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_con, connection_record):
    """Configurações específicas para PostgreSQL."""
    if "postgresql" in settings.DATABASE_URL:
        # Opcional: configurações específicas de PostgreSQL
        pass


def init_db() -> None:
    """Inicializa o banco de dados criando as tabelas."""
    from models.base import Base

    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Remove todas as tabelas do banco de dados."""
    from models.base import Base

    Base.metadata.drop_all(bind=engine)
