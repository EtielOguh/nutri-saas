"""Schemas base para validação de dados da API."""
from datetime import datetime
from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Schema base com configuração padrão."""

    model_config = ConfigDict(
        from_attributes=True,  # Permite usar modelos SQLAlchemy
        populate_by_name=True,  # Permite field names e aliases
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None,
        }
    )


class TimestampSchema(BaseSchema):
    """Schema com timestamp e ID."""

    id: int = Field(..., description="Identificador único")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de última atualização")


class SuccessResponse(BaseSchema):
    """Resposta de sucesso padrão."""

    message: str = Field(..., description="Mensagem de sucesso")
    data: Optional[dict] = Field(None, description="Dados da resposta")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Resposta paginada genérica."""

    total: int = Field(..., description="Total de itens")
    page: int = Field(..., ge=1, description="Página atual")
    page_size: int = Field(..., ge=1, le=100, description="Itens por página")
    items: List[T] = Field(..., description="Lista de itens")


class ErrorResponse(BaseSchema):
    """Resposta de erro padrão."""

    error: str = Field(..., description="Tipo de erro")
    detail: Optional[str] = Field(None, description="Detalhes do erro")
    status_code: int = Field(..., description="Código HTTP")
    status_code: int = Field(..., description="Código HTTP de status")
