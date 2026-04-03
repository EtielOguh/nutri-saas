"""Schemas para Token de Acesso do Cliente."""
from typing import Optional
from pydantic import Field

from schemas.base import BaseSchema, TimestampSchema


class TokenAcessoClienteBase(BaseSchema):
    """Schema base para Token de Acesso."""

    cliente_id: int = Field(..., gt=0, description="ID do cliente")
    token_unico: str = Field(..., min_length=20, max_length=255, description="Token único")


class TokenAcessoClienteCreate(BaseSchema):
    """Schema para criar Token (cliente_id fornecido na rota)."""

    cliente_id: int = Field(..., gt=0, description="ID do cliente")
    # token_unico é gerado automaticamente no serviço


class TokenAcessoClienteUpdate(BaseSchema):
    """Schema para regenerar Token."""

    # Não permite atualizar manualmente
    pass


class TokenAcessoClienteResponse(TimestampSchema, TokenAcessoClienteBase):
    """Schema de resposta para Token de Acesso."""

    cliente: Optional["ClienteSimpleResponse"] = Field(None, description="Cliente do token")  # noqa: F821


class TokenAcessoClienteGenerateResponse(BaseSchema):
    """Schema para resposta ao gerar novo token."""

    token_unico: str = Field(..., description="Token gerado")
    cliente_id: int = Field(..., description="ID do cliente")
    mensagem: str = Field(default="Token gerado com sucesso")


class TokenValidacaoResponse(BaseSchema):
    """Schema para validação de token."""

    valido: bool = Field(..., description="Se o token é válido")
    cliente_id: Optional[int] = Field(None, description="ID do cliente se válido")
    cliente_nome: Optional[str] = Field(None, description="Nome do cliente se válido")


class ClientePublicAccessResponse(BaseSchema):
    """Schema para acesso público via token.
    
    Retorna dados básicos do cliente e informações do token.
    """

    id: int = Field(..., description="ID do cliente")
    nome: str = Field(..., description="Nome do cliente")
    idade: Optional[int] = Field(None, description="Idade em anos")
    altura: Optional[float] = Field(None, description="Altura em cm")
    objetivo: Optional[str] = Field(None, description="Objetivo de saúde")
    token_criado_em: Optional[str] = Field(None, description="Data de criação do token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "João Silva",
                "idade": 30,
                "altura": 180,
                "objetivo": "Ganhar massa muscular",
                "token_criado_em": "2026-04-02T10:30:00"
            }
        }
