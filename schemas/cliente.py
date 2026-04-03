"""Schemas para Cliente."""
from typing import Optional, List
from pydantic import Field
from datetime import datetime

from schemas.base import BaseSchema, TimestampSchema
from schemas.nutricionista import NutricionistaSimpleResponse


class ClienteBase(BaseSchema):
    """Schema base para Cliente."""

    nutricionista_id: int = Field(..., gt=0, description="ID do nutricionista")
    nome: str = Field(..., min_length=3, max_length=255, description="Nome do cliente")
    idade: Optional[int] = Field(None, ge=1, le=150, description="Idade em anos")
    altura: Optional[float] = Field(None, gt=0, le=300, description="Altura em cm")
    objetivo: Optional[str] = Field(None, max_length=255, description="Objetivo de saúde")


class ClienteCreate(ClienteBase):
    """Schema para criar Cliente."""
    pass


class ClienteUpdate(BaseSchema):
    """Schema para atualizar Cliente."""

    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    idade: Optional[int] = Field(None, ge=1, le=150)
    altura: Optional[float] = Field(None, gt=0, le=300)
    objetivo: Optional[str] = Field(None, max_length=255)


class ClienteResponse(TimestampSchema, ClienteBase):
    """Schema de resposta para Cliente."""

    nutricionista: Optional[NutricionistaSimpleResponse] = Field(None, description="Nutricionista responsável")


class ClienteDetailResponse(ClienteResponse):
    """Schema de resposta detalhada para Cliente com acompanhamento."""

    # Relacionamentos
    total_medicoes: int = Field(default=0, description="Total de medições")
    total_observacoes: int = Field(default=0, description="Total de observações")
    total_documentos: int = Field(default=0, description="Total de documentos")
    ultimo_peso: Optional[float] = Field(None, description="Último peso registrado em kg")
    data_ultima_medicao: Optional[datetime] = Field(None, description="Data da última medição")


# Schema simplificado para relacionamentos
class ClienteSimpleResponse(BaseSchema):
    """Schema simples para Cliente (usado em relacionamentos)."""

    id: int
    nome: str
    idade: Optional[int] = None
    altura: Optional[float] = None
    objetivo: Optional[str] = None
