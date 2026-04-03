"""Rotas de autenticação."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.auth import LoginRequest, TokenResponse, NutricionistaLoginResponse
from schemas.base import ErrorResponse
from services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["autenticação"],
    responses={
        422: {"model": ErrorResponse, "description": "Erro de validação"},
        401: {"model": ErrorResponse, "description": "Credenciais inválidas"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
    },
)


@router.post(
    "/login",
    response_model=NutricionistaLoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login",
    description="Autentica um nutricionista e retorna um token JWT.",
)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> NutricionistaLoginResponse:
    """
    Autentica um nutricionista com email e senha.
    
    - **email**: Email do nutricionista
    - **senha**: Senha do nutricionista
    
    Retorna um token JWT que deve ser incluído no header Authorization.
    """
    service = AuthService(db=db)

    # Tenta autenticar
    nutricionista = service.authenticate_nutricionista(
        email=credentials.email,
        password=credentials.senha,
    )

    if not nutricionista:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Cria token
    token = service.create_access_token(nutricionista_id=nutricionista.id)

    return NutricionistaLoginResponse(
        id=nutricionista.id,
        nome=nutricionista.nome,
        email=nutricionista.email,
        crn=nutricionista.crn,
        token=token,
    )


@router.post(
    "/verify",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Verificar token",
    description="Verifica se um token JWT é válido.",
)
async def verify_token(
    token: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Verifica se um token JWT é válido.
    
    - **token**: Token JWT
    
    Retorna os dados do nutricionista se o token for válido.
    """
    service = AuthService(db=db)

    nutricionista_id = service.verify_token(token)

    if not nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from models.nutricionista import Nutricionista

    nutricionista = db.query(Nutricionista).filter(
        Nutricionista.id == nutricionista_id
    ).first()

    if not nutricionista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nutricionista não encontrado",
        )

    return {
        "id": nutricionista.id,
        "nome": nutricionista.nome,
        "email": nutricionista.email,
    }
