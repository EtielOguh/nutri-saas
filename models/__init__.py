"""Models module - modelos de banco de dados SQLAlchemy."""

# Importar Base primeiro (não depende de nada)
from models.base import Base, BaseModel

# Importar modelos (strings em relationship evitam problemas de circular imports)
from models.nutricionista import Nutricionista, ConfiguracaoNutricionista
from models.cliente import Cliente
from models.medicao import Medicao
from models.observacao import Observacao
from models.token_acesso import TokenAcessoCliente
from models.documento import DocumentoPDF

# Exportar para facilitar imports
__all__ = [
    "Base",
    "BaseModel",
    "Nutricionista",
    "ConfiguracaoNutricionista",
    "Cliente",
    "Medicao",
    "Observacao",
    "TokenAcessoCliente",
    "DocumentoPDF",
]
