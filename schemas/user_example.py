"""
Exemplo de schema de usuário.

Este é um arquivo de exemplo mostrando como criar schemas Pydantic
para validar dados de entrada e saída
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Schema base com campos comuns."""

    email: EmailStr = Field(..., description="Email do usuário")
    name: str = Field(..., min_length=1, max_length=255, description="Nome do usuário")


class UserCreate(UserBase):
    """Schema para criar um novo usuário."""

    password: str = Field(
        ..., min_length=8, max_length=255, description="Senha do usuário"
    )


class UserUpdate(BaseModel):
    """Schema para atualizar um usuário."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema de resposta com dados do usuário."""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponseWithPassword(UserResponse):
    """Schema completo (apenas para uso interno, não retornar ao cliente)."""

    password_hash: str
