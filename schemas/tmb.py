"""
Schemas Pydantic para cálculo de TMB (Taxa Metabólica Basal).

Define as estruturas de requisição e resposta para os endpoints de TMB.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class TMBRequest(BaseModel):
    """Schema para requisição de cálculo de TMB."""

    peso_kg: float = Field(
        ...,
        ge=1,
        le=635,
        title="Peso",
        description="Peso corporal em quilogramas",
        example=70.5,
    )
    altura_cm: float = Field(
        ...,
        ge=50,
        le=300,
        title="Altura",
        description="Altura en centímetros",
        example=180.0,
    )
    idade_anos: int = Field(
        ...,
        ge=1,
        le=150,
        title="Idade",
        description="Idade em anos",
        example=30,
    )
    sexo: Literal["M", "F"] = Field(
        ...,
        title="Sexo",
        description="Sexo biológico (M = Masculino, F = Feminino)",
        example="M",
    )

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, v: str) -> str:
        """Validar e normalizar sexo para maiúscula."""
        if v.upper() not in ("M", "F"):
            raise ValueError("sexo deve ser 'M' (Masculino) ou 'F' (Feminino)")
        return v.upper()

    class Config:
        """Configuração do modelo."""

        json_schema_extra = {
            "example": {
                "peso_kg": 70.5,
                "altura_cm": 180.0,
                "idade_anos": 30,
                "sexo": "M",
            }
        }


class TMBResponse(BaseModel):
    """Schema para resposta de cálculo de TMB."""

    tmb: float = Field(
        title="Taxa Metabólica Basal",
        description="Calorias necessárias em repouso (kcal/dia)",
        example=1662.25,
    )
    peso_kg: float = Field(title="Peso", example=70.5)
    altura_cm: float = Field(title="Altura", example=180.0)
    idade_anos: int = Field(title="Idade", example=30)
    sexo: str = Field(title="Sexo", example="M")

    class Config:
        """Configuração do modelo."""

        json_schema_extra = {
            "example": {
                "tmb": 1662.25,
                "peso_kg": 70.5,
                "altura_cm": 180.0,
                "idade_anos": 30,
                "sexo": "M",
            }
        }


class GastoCaloricRequest(BaseModel):
    """Schema para requisição de cálculo de gasto calórico (TDEE)."""

    peso_kg: float = Field(
        ...,
        ge=1,
        le=635,
        title="Peso",
        description="Peso corporal em quilogramas",
        example=70.5,
    )
    altura_cm: float = Field(
        ...,
        ge=50,
        le=300,
        title="Altura",
        description="Altura en centímetros",
        example=180.0,
    )
    idade_anos: int = Field(
        ...,
        ge=1,
        le=150,
        title="Idade",
        description="Idade em anos",
        example=30,
    )
    sexo: Literal["M", "F"] = Field(
        ...,
        title="Sexo",
        description="Sexo biológico (M = Masculino, F = Feminino)",
        example="M",
    )
    nivel_atividade: Literal[
        "sedentario", "leve", "moderado", "intenso", "muito_intenso"
    ] = Field(
        ...,
        title="Nível de Atividade",
        description=(
            "Nível de atividade física:\n"
            "- sedentario: Pouco ou nenhum exercício\n"
            "- leve: 1-3 dias por semana\n"
            "- moderado: 3-5 dias por semana\n"
            "- intenso: 6-7 dias por semana\n"
            "- muito_intenso: 2x por dia ou trabalho físico"
        ),
        example="moderado",
    )

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, v: str) -> str:
        """Validar e normalizar sexo para maiúscula."""
        if v.upper() not in ("M", "F"):
            raise ValueError("sexo deve ser 'M' ou 'F'")
        return v.upper()

    class Config:
        """Configuração do modelo."""

        json_schema_extra = {
            "example": {
                "peso_kg": 70.5,
                "altura_cm": 180.0,
                "idade_anos": 30,
                "sexo": "M",
                "nivel_atividade": "moderado",
            }
        }


class GastoCaloricResponse(BaseModel):
    """Schema para resposta de gasto calórico (TDEE)."""

    tmb: float = Field(
        title="Taxa Metabólica Basal",
        description="Calorias em repouso (kcal/dia)",
        example=1662.25,
    )
    fator_atividade: float = Field(
        title="Fator de Atividade",
        description="Multiplicador aplicado à TMB",
        example=1.55,
    )
    nivel_atividade: str = Field(
        title="Nível de Atividade", description="Nível utilizado", example="moderado"
    )
    tdee: float = Field(
        title="Gasto Energético Diário Total",
        description="Calorias totais necessárias (kcal/dia)",
        example=2576.49,
    )
    deficit_leve: float = Field(
        title="Déficit Calórico Leve",
        description="Calorias para perda de ~250g/semana (kcal/dia)",
        example=2076.49,
    )
    deficit_moderado: float = Field(
        title="Déficit Calórico Moderado",
        description="Calorias para perda de ~375g/semana (kcal/dia)",
        example=1826.49,
    )
    superavit_leve: float = Field(
        title="Superávit Calórico Leve",
        description="Calorias para ganho de ~250g/semana (kcal/dia)",
        example=3076.49,
    )
    superavit_moderado: float = Field(
        title="Superávit Calórico Moderado",
        description="Calorias para ganho de ~375g/semana (kcal/dia)",
        example=3326.49,
    )
    peso_kg: float = Field(title="Peso", example=70.5)
    altura_cm: float = Field(title="Altura", example=180.0)
    idade_anos: int = Field(title="Idade", example=30)
    sexo: str = Field(title="Sexo", example="M")

    class Config:
        """Configuração do modelo."""

        json_schema_extra = {
            "example": {
                "tmb": 1662.25,
                "fator_atividade": 1.55,
                "nivel_atividade": "moderado",
                "tdee": 2576.49,
                "deficit_leve": 2076.49,
                "deficit_moderado": 1826.49,
                "superavit_leve": 3076.49,
                "superavit_moderado": 3326.49,
                "peso_kg": 70.5,
                "altura_cm": 180.0,
                "idade_anos": 30,
                "sexo": "M",
            }
        }


class IndiceIMC(BaseModel):
    """Schema com cálculo de IMC."""

    imc: float = Field(
        title="Índice de Massa Corporal",
        description="IMC = peso / (altura em metros)²",
        example=21.7,
    )
    classificacao: str = Field(
        title="Classificação",
        description="Classificação de peso baseada no IMC",
        example="Peso normal",
    )

    class Config:
        """Configuração do modelo."""

        json_schema_extra = {"example": {"imc": 21.7, "classificacao": "Peso normal"}}


class TMBComIMCResponse(TMBResponse):
    """Schema de TMB com cálculo de IMC incluído."""

    imc: float = Field(
        title="Índice de Massa Corporal", description="IMC", example=21.7
    )
    imc_classificacao: str = Field(
        title="Classificação de Peso", description="Classificação baseada no IMC", example="Peso normal"
    )

    class Config:
        """Configuração do modelo."""

        json_schema_extra = {
            "example": {
                "tmb": 1662.25,
                "peso_kg": 70.5,
                "altura_cm": 180.0,
                "idade_anos": 30,
                "sexo": "M",
                "imc": 21.7,
                "imc_classificacao": "Peso normal",
            }
        }
