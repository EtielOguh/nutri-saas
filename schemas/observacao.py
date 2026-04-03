"""Schemas para Observação."""
from typing import Optional
from pydantic import Field

from schemas.base import BaseSchema, TimestampSchema
from schemas.cliente import ClienteSimpleResponse


class ObservacaoBase(BaseSchema):
    """Schema base para Observação."""

    cliente_id: int = Field(..., gt=0, description="ID do cliente")
    texto: str = Field(..., min_length=1, max_length=5000, description="Texto da observação")


class ObservacaoCreate(ObservacaoBase):
    """Schema para criar Observação."""
    pass


class ObservacaoUpdate(BaseSchema):
    """Schema para atualizar Observação."""

    texto: str = Field(..., min_length=1, max_length=5000)


class ObservacaoResponse(TimestampSchema, ObservacaoBase):
    """Schema de resposta para Observação."""

    cliente: Optional[ClienteSimpleResponse] = Field(None, description="Cliente da observação")


class ObservacaoSimpleResponse(BaseSchema):
    """Schema simples para Observação."""

    id: int
    texto: str
    created_at: str = Field(..., description="Data da observação")
