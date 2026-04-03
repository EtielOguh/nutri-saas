"""Schemas module - validação de dados com Pydantic."""

# Base schemas
from schemas.base import (
    BaseSchema,
    TimestampSchema,
    PaginatedResponse,
    ErrorResponse,
)

# Nutricionista schemas
from schemas.nutricionista import (
    ConfiguracaoNutricionistaBase,
    ConfiguracaoNutricionistaCreate,
    ConfiguracaoNutricionistaUpdate,
    ConfiguracaoNutricionistaResponse,
    NutricionistaBase,
    NutricionistaCreate,
    NutricionistaUpdate,
    NutricionistaResponse,
    NutricionistaDetailResponse,
    NutricionistaSimpleResponse,
)

# Cliente schemas
from schemas.cliente import (
    ClienteBase,
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteDetailResponse,
    ClienteSimpleResponse,
)

# Medicao schemas
from schemas.medicao import (
    MedicaoBase,
    MedicaoCreate,
    MedicaoUpdate,
    MedicaoResponse,
    MedicaoSimpleResponse,
    MedicaoHistoricoResponse,
)

# Observacao schemas
from schemas.observacao import (
    ObservacaoBase,
    ObservacaoCreate,
    ObservacaoUpdate,
    ObservacaoResponse,
    ObservacaoSimpleResponse,
)

# TokenAcesso schemas
from schemas.token_acesso import (
    TokenAcessoClienteBase,
    TokenAcessoClienteCreate,
    TokenAcessoClienteUpdate,
    TokenAcessoClienteResponse,
    TokenAcessoClienteGenerateResponse,
    TokenValidacaoResponse,
)

# Documento schemas
from schemas.documento import (
    DocumentoPDFBase,
    DocumentoPDFCreate,
    DocumentoPDFUpdate,
    DocumentoPDFResponse,
    DocumentoPDFSimpleResponse,
    DocumentoPDFBulkResponse,
)

__all__ = [
    # Base
    "BaseSchema",
    "TimestampSchema",
    "PaginatedResponse",
    "ErrorResponse",
    # Nutricionista
    "ConfiguracaoNutricionistaBase",
    "ConfiguracaoNutricionistaCreate",
    "ConfiguracaoNutricionistaUpdate",
    "ConfiguracaoNutricionistaResponse",
    "NutricionistaBase",
    "NutricionistaCreate",
    "NutricionistaUpdate",
    "NutricionistaResponse",
    "NutricionistaDetailResponse",
    "NutricionistaSimpleResponse",
    # Cliente
    "ClienteBase",
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    "ClienteDetailResponse",
    "ClienteSimpleResponse",
    # Medicao
    "MedicaoBase",
    "MedicaoCreate",
    "MedicaoUpdate",
    "MedicaoResponse",
    "MedicaoSimpleResponse",
    "MedicaoHistoricoResponse",
    # Observacao
    "ObservacaoBase",
    "ObservacaoCreate",
    "ObservacaoUpdate",
    "ObservacaoResponse",
    "ObservacaoSimpleResponse",
    # TokenAcesso
    "TokenAcessoClienteBase",
    "TokenAcessoClienteCreate",
    "TokenAcessoClienteUpdate",
    "TokenAcessoClienteResponse",
    "TokenAcessoClienteGenerateResponse",
    "TokenValidacaoResponse",
    # Documento
    "DocumentoPDFBase",
    "DocumentoPDFCreate",
    "DocumentoPDFUpdate",
    "DocumentoPDFResponse",
    "DocumentoPDFSimpleResponse",
    "DocumentoPDFBulkResponse",
]
