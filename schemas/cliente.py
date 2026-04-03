"""Schemas para Cliente."""
from typing import Optional, List
from pydantic import Field, field_validator
from datetime import datetime

from schemas.base import BaseSchema, TimestampSchema
from schemas.nutricionista import NutricionistaSimpleResponse


class ClienteBase(BaseSchema):
    """Schema base para Cliente."""

    nutricionista_id: int = Field(..., gt=0, description="ID do nutricionista")
    nome: str = Field(..., min_length=3, max_length=255, description="Nome do cliente")
    email: Optional[str] = Field(None, max_length=255, description="Email do cliente")
    phone: Optional[str] = Field(None, max_length=20, description="Telefone do cliente")
    idade: Optional[int] = Field(None, ge=1, le=150, description="Idade em anos")
    altura: Optional[float] = Field(None, gt=0, le=300, description="Altura em cm")
    gender: Optional[str] = Field(None, max_length=20, description="Gênero")
    initial_weight: Optional[float] = Field(None, gt=0, description="Peso inicial em kg")
    objetivo: Optional[str] = Field(None, max_length=255, description="Objetivo de saúde")
    notes: Optional[str] = Field(None, description="Notas adicionais")


class ClienteCreate(BaseSchema):
    """Schema para criar Cliente - aceita tanto en quanto pt-BR."""
    
    nutricionista_id: int = Field(..., gt=0, description="ID do nutricionista")
    # Aceita ambos os nomes (português e inglês)
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    
    idade: Optional[int] = Field(None, ge=1, le=150)
    age: Optional[int] = Field(None, ge=1, le=150)
    
    altura: Optional[float] = Field(None, gt=0, le=300)
    height: Optional[float] = Field(None, gt=0, le=300)
    
    objetivo: Optional[str] = Field(None, max_length=255)
    objective: Optional[str] = Field(None, max_length=255)
    
    # Campos adicionais que podem vir do frontend
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=20)
    initial_weight: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None)
    
    @field_validator('nome', mode='before')
    @classmethod
    def validate_nome(cls, v, info):
        """Usa 'name' se 'nome' não foi fornecido."""
        if v is None and 'name' in info.data:
            return info.data.get('name')
        return v
    
    @field_validator('idade', mode='before')
    @classmethod
    def validate_idade(cls, v, info):
        """Usa 'age' se 'idade' não foi fornecido."""
        if v is None and 'age' in info.data:
            return info.data.get('age')
        return v
    
    @field_validator('altura', mode='before')
    @classmethod
    def validate_altura(cls, v, info):
        """Usa 'height' se 'altura' não foi fornecido."""
        if v is None and 'height' in info.data:
            return info.data.get('height')
        return v
    
    @field_validator('objetivo', mode='before')
    @classmethod
    def validate_objetivo(cls, v, info):
        """Usa 'objective' se 'objetivo' não foi fornecido."""
        if v is None and 'objective' in info.data:
            return info.data.get('objective')
        return v
    
    def get_validated_data(self) -> dict:
        """Retorna apenas os campos necessários para ClienteBase."""
        return {
            'nutricionista_id': self.nutricionista_id,
            'nome': self.nome or self.name,
            'email': self.email,
            'phone': self.phone,
            'idade': self.idade or self.age,
            'altura': self.altura or self.height,
            'gender': self.gender,
            'initial_weight': self.initial_weight,
            'objetivo': self.objetivo or self.objective,
            'notes': self.notes,
        }


class ClienteUpdate(BaseSchema):
    """Schema para atualizar Cliente."""

    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    
    idade: Optional[int] = Field(None, ge=1, le=150)
    age: Optional[int] = Field(None, ge=1, le=150)
    
    altura: Optional[float] = Field(None, gt=0, le=300)
    height: Optional[float] = Field(None, gt=0, le=300)
    
    objetivo: Optional[str] = Field(None, max_length=255)
    objective: Optional[str] = Field(None, max_length=255)


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


class ClientePublicResponse(BaseSchema):
    """Schema de resposta pública para Cliente (acesso via token).
    
    Retorna apenas dados básicos, sem informações sensíveis.
    Usado para endpoint público /cliente/{token}
    """

    id: int = Field(..., description="ID do cliente")
    nome: str = Field(..., description="Nome do cliente")
    idade: Optional[int] = Field(None, description="Idade em anos")
    altura: Optional[float] = Field(None, description="Altura em cm")
    objetivo: Optional[str] = Field(None, description="Objetivo de saúde")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "João Silva",
                "idade": 30,
                "altura": 180,
                "objetivo": "Ganhar massa muscular"
            }
        }
