"""
Dependências de banco de dados para injeção em rotas.

Exemplo de uso em uma rota:

    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from core.database import get_db
    from services.user_service import UserService
    
    router = APIRouter(prefix="/users", tags=["users"])
    
    @router.get("/")
    async def list_users(db: Session = Depends(get_db)):
        service = UserService(db=db)
        return service.get_all()
"""

from sqlalchemy.orm import Session
from core.database import SessionLocal


async def get_db_session() -> Session:
    """
    Dependency alternativo para injetar a sessão do banco em rotas assíncronas.
    
    Yields:
        Session: Sessão ativa do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
