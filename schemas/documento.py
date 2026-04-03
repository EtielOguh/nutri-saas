"""Schemas para Documento PDF."""
from typing import Optional
from pydantic import Field, HttpUrl

from schemas.base import BaseSchema, TimestampSchema
from schemas.cliente import ClienteSimpleResponse


class DocumentoPDFBase(BaseSchema):
    """Schema base para Documento PDF."""

    cliente_id: int = Field(..., gt=0, description="ID do cliente")
    url_pdf: str = Field(..., max_length=512, description="URL do arquivo PDF")


class DocumentoPDFCreate(DocumentoPDFBase):
    """Schema para criar Documento PDF."""
    pass


class DocumentoPDFUpdate(BaseSchema):
    """Schema para atualizar Documento PDF."""

    url_pdf: str = Field(..., max_length=512, description="URL do arquivo PDF")


class DocumentoPDFResponse(TimestampSchema, DocumentoPDFBase):
    """Schema de resposta para Documento PDF."""

    cliente: Optional[ClienteSimpleResponse] = Field(None, description="Cliente do documento")


class DocumentoPDFSimpleResponse(BaseSchema):
    """Schema simples para Documento PDF."""

    id: int
    url_pdf: str
    created_at: str = Field(..., description="Data de upload")


class DocumentoPDFBulkResponse(BaseSchema):
    """Schema para resposta de upload em lote."""

    total: int = Field(..., description="Total de documentos")
    sucesso: int = Field(..., description="Documentos cadastrados com sucesso")
    erro: int = Field(..., description="Documentos com erro")
    detalhes: Optional[list] = Field(None, description="Detalhes dos erros")
