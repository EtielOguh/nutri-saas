"""Schemas base para respostas da API."""
from datetime import datetime
from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Schema base com validações comuns."""

    class Config:
        from_attributes = True


class TimestampSchema(BaseSchema):
    """Schema com campos de timestamp."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseSchema, Generic[T]):
    """Resposta paginada genérica."""

    total: int = Field(..., description="Total de itens")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Itens por página")
    items: List[T] = Field(..., description="Lista de itens")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 100,
                "page": 1,
                "page_size": 10,
                "items": [],
            }
        }


class ErrorResponse(BaseSchema):
    """Resposta de erro padrão."""

    error: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais")
    status_code: int = Field(..., description="Código HTTP de status")
