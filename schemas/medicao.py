"""Schemas para Medição."""
from typing import Optional, List
from pydantic import Field
from datetime import datetime

from schemas.base import BaseSchema, TimestampSchema
from schemas.cliente import ClienteSimpleResponse


class MedicaoBase(BaseSchema):
    """Schema base para Medição."""

    cliente_id: int = Field(..., gt=0, description="ID do cliente")
    peso: float = Field(..., gt=0, le=1000, description="Peso em kg")


class MedicaoCreate(MedicaoBase):
    """Schema para criar Medição."""
    pass


class MedicaoUpdate(BaseSchema):
    """Schema para atualizar Medição."""

    peso: float = Field(..., gt=0, le=1000, description="Peso em kg")


class MedicaoResponse(TimestampSchema, MedicaoBase):
    """Schema de resposta para Medição."""

    data_medicao: datetime = Field(..., description="Data da medição")
    cliente: Optional[ClienteSimpleResponse] = Field(None, description="Cliente medido")


class MedicaoSimpleResponse(BaseSchema):
    """Schema simples para Medição."""

    id: int
    peso: float
    data_medicao: datetime


class MedicaoHistoricoResponse(BaseSchema):
    """Schema para histórico de medições."""

    total: int = Field(..., description="Total de medições")
    medicoes: List[MedicaoResponse] = Field(..., description="Lista de medições")
    variacao_total: Optional[float] = Field(None, description="Variação total em kg")
    percentual_variacao: Optional[float] = Field(None, description="Percentual de variação")
