"""
Dependências de banco de dados e autenticação para injeção em rotas.

Exemplo de uso em uma rota:

    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from core.database import get_db
    from core.dependencies import get_current_user
    from models.nutricionista import Nutricionista
    from services.user_service import UserService
    
    router = APIRouter(prefix="/users", tags=["users"])
    
    @router.get("/")
    async def list_users(
        db: Session = Depends(get_db),
        current_user: Nutricionista = Depends(get_current_user)
    ):
        service = UserService(db=db)
        return service.get_all()
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import SessionLocal, get_db
from services.auth_service import AuthService
from models.nutricionista import Nutricionista

security = HTTPBearer()


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


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Nutricionista:
    """
    Valida o token JWT do header Authorization e retorna o usuário autenticado.
    
    Args:
        credentials: Credenciais do header Authorization (formato: Bearer <token>)
        db: Sessão do banco de dados
        
    Returns:
        Nutricionista autenticado
        
    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    token = credentials.credentials
    
    auth_service = AuthService(db=db)
    nutricionista_id = auth_service.verify_token(token)
    
    if nutricionista_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se o nutricionista existe no banco
    nutricionista = db.query(Nutricionista).filter(
        Nutricionista.id == nutricionista_id
    ).first()
    
    if not nutricionista:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nutricionista não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return nutricionista
