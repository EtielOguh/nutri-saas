"""Schemas para Nutricionista."""
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, StringConstraints
from datetime import datetime

from schemas.base import BaseSchema, TimestampSchema


class ConfiguracaoNutricionistaBase(BaseSchema):
    """Schema base para Configuração."""

    logo_url: Optional[str] = Field(None, max_length=512, description="URL da logo")
    cor_primaria: str = Field(default="#0066CC", pattern="^#[0-9A-Fa-f]{6}$", description="Cor em formato hex")
    valor_consulta: float = Field(..., gt=0, description="Valor da consulta em R$")
    link_agendamento: Optional[str] = Field(None, max_length=512, description="Link para agendamento")


class ConfiguracaoNutricionistaCreate(ConfiguracaoNutricionistaBase):
    """Schema para criar configuração."""
    pass


class ConfiguracaoNutricionistaUpdate(BaseSchema):
    """Schema para atualizar configuração."""

    logo_url: Optional[str] = Field(None, max_length=512)
    cor_primaria: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    valor_consulta: Optional[float] = Field(None, gt=0)
    link_agendamento: Optional[str] = Field(None, max_length=512)


class ConfiguracaoNutricionistaResponse(TimestampSchema, ConfiguracaoNutricionistaBase):
    """Schema de resposta para Configuração."""

    nutricionista_id: int


class NutricionistaBase(BaseSchema):
    """Schema base para Nutricionista."""

    nome: str = Field(..., min_length=3, max_length=255, description="Nome do nutricionista")
    email: EmailStr = Field(..., description="Email único do nutricionista")


class NutricionistaCreate(NutricionistaBase):
    """Schema para criar Nutricionista."""

    senha: str = Field(..., min_length=8, description="Senha (mínimo 8 caracteres)")


class NutricionistaUpdate(BaseSchema):
    """Schema para atualizar Nutricionista."""

    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None


class NutricionistaResponse(TimestampSchema, NutricionistaBase):
    """Schema de resposta para Nutricionista."""

    configuracao: Optional[ConfiguracaoNutricionistaResponse] = Field(None, description="Configurações do nutricionista")


class NutricionistaDetailResponse(NutricionistaResponse):
    """Schema de resposta detalhada para Nutricionista com clientes."""

    total_clientes: int = Field(default=0, description="Total de clientes")


# Schema simplificado para relacionamentos
class NutricionistaSimpleResponse(BaseSchema):
    """Schema simples para Nutricionista (usado em relacionamentos)."""

    id: int
    nome: str
    email: str


class LogoUploadResponse(BaseSchema):
    """Schema de resposta para upload de logo."""

    nutricionista_id: int = Field(..., description="ID do nutricionista")
    logo_url: str = Field(..., description="URL da logo armazenada")
    logo_path: str = Field(..., description="Caminho relativo do arquivo")
    file_size: int = Field(..., ge=0, description="Tamanho do arquivo em bytes")
    message: str = Field(..., description="Mensagem de sucesso")


class DashboardClienteInfo(BaseSchema):
    """Informações básicas de um cliente para o dashboard."""

    id: int = Field(..., description="ID do cliente")
    nome: str = Field(..., description="Nome do cliente")
    idade: Optional[int] = Field(None, description="Idade do cliente")
    objetivo: Optional[str] = Field(None, description="Objetivo do cliente")
    ultima_medicao: Optional[float] = Field(None, description="Peso da última medição em kg")
    data_ultima_medicao: Optional[datetime] = Field(None, description="Data da última medição")


class DashboardMetricas(BaseSchema):
    """Métricas agregadas do dashboard."""

    total_clientes: int = Field(..., ge=0, description="Total de clientes do nutricionista")
    total_medicoes: int = Field(..., ge=0, description="Total de medições registradas")
    media_peso: Optional[float] = Field(None, description="Média de peso de todos os clientes em kg")
    num_clientes_ativos: int = Field(..., ge=0, description="Clientes com medições no último mês")


class DashboardNutricionistaResponse(BaseSchema):
    """Resposta completa do dashboard do nutricionista."""

    nutricionista_id: int = Field(..., description="ID do nutricionista")
    nome: str = Field(..., description="Nome do nutricionista")
    email: str = Field(..., description="Email do nutricionista")
    metricas: DashboardMetricas = Field(..., description="Métricas agregadas")
    clientes_recentes: List[DashboardClienteInfo] = Field(
        ..., description="Últimos 5 clientes com atividade recente"
    )
    configuracao: Optional[ConfiguracaoNutricionistaResponse] = Field(
        None, description="Configurações do nutricionista"
    )
