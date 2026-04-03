"""Schemas de autenticação."""
from pydantic import BaseModel, Field, EmailStr

from schemas.base import BaseSchema


class LoginRequest(BaseSchema):
    """Requisição de login."""

    email: EmailStr = Field(..., description="Email do nutricionista")
    senha: str = Field(..., min_length=6, description="Senha do nutricionista")


class TokenResponse(BaseSchema):
    """Resposta com token de acesso."""

    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    nutricionista_id: int = Field(..., description="ID do nutricionista")
    nome: str = Field(..., description="Nome do nutricionista")
    email: str = Field(..., description="Email do nutricionista")


class NutricionistaLoginResponse(BaseSchema):
    """Resposta com dados do nutricionista após login."""

    id: int = Field(..., description="ID do nutricionista")
    nome: str = Field(..., description="Nome do nutricionista")
    email: str = Field(..., description="Email do nutricionista")
    token: str = Field(..., description="Token JWT")
